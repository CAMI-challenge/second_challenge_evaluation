import pandas as pd
import os
from jinja2 import Template
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.plotting import ColumnDataSource
from bokeh.models import DataTable, CustomJS
from bokeh.models.widgets import TableColumn, Slider, Div, Panel, Tabs
from bokeh.embed import components
from bokeh.resources import INLINE


pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

METRICS_ASSEMB_L = ['Sum of scores', 'Strain recall', 'Strain precision', '# mismatches per 100 kbp', 'Duplication ratio', '# misassemblies', 'Genome fraction (%)', 'NGA50']
METRICS_ASSEMB = {'Strain recall': 'recall',
                  'Strain precision': 'precision',
                  '# mismatches per 100 kbp': 'mismatches',
                  'Duplication ratio': 'duplication',
                  '# misassemblies': 'misassemblies',
                  'Genome fraction (%)': 'fraction',
                  'NGA50': 'nga50',
                  'Sum of scores': 'sum'}

METRICS_GBIN_L = ['Sum of scores', 'CAMI 1 average completeness (bp)', 'Average purity (bp)', 'Adjusted Rand index (bp)', 'Percentage of binned bp']
METRICS_GBIN = {'CAMI 1 average completeness (bp)': 'completeness',
                'Average purity (bp)': 'purity',
                'Adjusted Rand index (bp)': 'ari',
                'Percentage of binned bp': 'binnedbp',
                'Sum of scores': 'sum'}


def create_rankings_html(pd_res, pd_table, source, tab_title, title, metrics_list, metrics_dict):
    jscript = 'topx[i] = '
    for metric in metrics_list[1:]:
        jscript += "data['" + metrics_dict[metric] + "'][i] * weight_" + metrics_dict[metric] + ".value +"
    jscript = jscript[:-1] + ';'

    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var topx = data['top'];
        for (let i = 0; i < topx.length; i++) {""" + jscript + """ }
        console.log(data['top'].length);
        source.change.emit();
    """)

    sliders_list = []
    for metric in metrics_list[1:]:
        slider = Slider(start=0, end=10, value=1, step=.1, title=metric + ' weight')
        slider.js_on_change('value', callback)
        callback.args['weight_' + metrics_dict[metric]] = slider
        sliders_list.append(slider)

    p = figure(x_range=list(pd_res.sort_values('Sum of scores')['tool']), plot_width=1200, plot_height=500, title="Sum of scores - lower is better")
    p.vbar(x='x', top='top', source=source, width=0.5, bottom=0, color="firebrick")
    p.xaxis.major_label_orientation = 1

    columns = []
    for metric in metrics_list:
        columns.append(TableColumn(field=metric, title=metric, sortable=False, width=190))
        columns.append(TableColumn(field='score' + metric, title='', width=20))

    table_source = ColumnDataSource(pd_table)
    data_table = DataTable(source=table_source, columns=columns, width=1800, height=25 + len(pd_table) * 25, autosize_mode = 'none') #fit_columns=False

    title_div = Div(text=title, style={"width": "1000px", "margin-top": "18px", "font-size": "18pt"})
    if len(sliders_list) > 4:
        return Panel(child=column(title_div, data_table, row(sliders_list[0:4]), row(sliders_list[4:]), p), title=tab_title)
    else:
        return Panel(child=column(title_div, data_table, row(sliders_list), p), title=tab_title)


def format_pd(pd_res):
    pd_table = pd_res.set_index('tool').stack().reset_index().rename(columns={'level_1': 'metric', 0: 'value'})

    df_list = []
    for metric, g in pd_table.groupby('metric'):
        x = g.sort_values('value')
        df_list.append(pd.DataFrame({metric: x['tool'].tolist(), 'score' + metric: x['value'].tolist()}))

    return pd.concat(df_list, axis=1)


def get_source_assemblers(pd_res):
    return ColumnDataSource(data=dict(x=pd_res['tool'],
                            top=pd_res['Sum of scores'],
                            recall=pd_res['Strain recall'],
                            precision=pd_res['Strain precision'],
                            mismatches=pd_res['# mismatches per 100 kbp'],
                            duplication=pd_res['Duplication ratio'],
                            misassemblies=pd_res['# misassemblies'],
                            fraction=pd_res['Genome fraction (%)'],
                            nga50=pd_res['NGA50']))


def get_source_genome_binners(pd_res):
    return ColumnDataSource(data=dict(x=pd_res['tool'],
                            top=pd_res['Sum of scores'],
                            completeness=pd_res['CAMI 1 average completeness (bp)'],
                            purity=pd_res['Average purity (bp)'],
                            ari=pd_res['Adjusted Rand index (bp)'],
                            binnedbp=pd_res['Percentage of binned bp']))


def read_genome_binning_scores(file):
    binning = pd.read_csv(file, sep='\t', index_col=0)
    binning.columns = binning.columns.str.replace(r'rank$', '')
    binning = binning.rename(columns={'sum': 'Sum of scores'})

    df_list = []
    for metric in METRICS_GBIN_L:
        x = binning[metric].str.extract(r'(.*\(\D\d\))\s\((\d*)\)').rename(columns={0: metric, 1: 'score' + metric})
        x['score' + metric] = x['score' + metric].astype('int32')
        x = x.sort_values('score' + metric)
        df_list.append(x)

    df_list2 = []
    for df in df_list:
        df_list2.append(df.rename(columns={df.columns[0]: 'tool', df.columns[1]: df.columns[1][5:]}).set_index('tool'))
    return pd.concat(df_list2, axis=1).reset_index().rename(columns={'index': 'tool'}), pd.concat(df_list, axis=1)


def create_html():

    template = Template('''<!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <title>OPAL: Open-community Profiling Assessment tooL</title>
                {{ js_resources }}
                {{ css_resources }}
                <style>.bk-fit-content {width: fit-content; width: -moz-fit-content;}
                .bk-width-auto {width: auto !important;}
                .bk-height-auto {height: auto !important;}
                .bk-inline-block {display: inline-block !important; float: left;}
                .bk-width-auto-main>div {width: -webkit-fill-available !important;}
                div.bk-width-auto-main {width: -webkit-fill-available !important;}
                div.bk.bk-tabs-margin{top: 30px !important;}
                .bk-tabs-margin-lr{margin-left: 10px; margin-right: 10px}
                .bk-root {display: flex; justify-content: center;}
                .bk-padding-top {padding-top: 10px;}
                html {overflow: -moz-scrollbars-vertical; overflow-y: scroll;}
                tr:hover {outline: 1px solid black;}
                .proportions {
                    cursor: pointer;
                }
                .legend {
                    position:absolute;
                    cursor: move;
                    z-index: 1;
                }
                </style>
            </head>
            <body>
                {{ div }}
                {{ script }}
                <script>
                    showlegend = function(img, elementid){
                        var x = document.getElementById(elementid);
                        if (x.style.visibility == 'visible') {
                            x.style.visibility = 'hidden';
                            x.style.display = 'none';
                        } else {
                            if (!x.style.top) {
                                x.style.top = img.offsetTop.toString().concat('px');
                            }
                            if (!x.style.left) {
                                x.style.left = img.offsetLeft.toString().concat('px');
                            }
                            x.style.visibility = 'visible';
                            x.style.display = 'initial';
                        }
                    }
                    function startDrag(e) {
                        if (!e) {
                            var e = window.event;
                        }
                        targ = e.target ? e.target : e.srcElement;
                        if (targ.className != 'legend') {return};
                        offsetX = e.clientX;
                        offsetY = e.clientY;
                        coordX = parseInt(targ.style.left);
                        coordY = parseInt(targ.style.top);
                        drag = true;
                        document.onmousemove=dragDiv;
                        return false;
                    }
                    function dragDiv(e) {
                        if (!drag) {return};
                        if (!e) { var e= window.event};
                        targ.style.left=coordX+e.clientX-offsetX+'px';
                        targ.style.top=coordY+e.clientY-offsetY+'px';
                        return false;
                    }
                    function stopDrag() {
                        drag=false;
                    }
                    window.onload = function() {
                        document.onmousedown = startDrag;
                        document.onmouseup = stopDrag;
                    }
                </script>
            </body>
        </html>
        ''')

    pd_res = pd.read_csv('../assembly/rankings/assemblers_marine.csv', sep='\t')
    tab1 = create_rankings_html(pd_res, format_pd(pd_res), get_source_assemblers(pd_res), "Marine", "Assemblers - Marine dataset", METRICS_ASSEMB_L, METRICS_ASSEMB)

    pd_res = pd.read_csv('../assembly/rankings/assemblers_marine_common.csv', sep='\t')
    tab2 = create_rankings_html(pd_res, format_pd(pd_res), get_source_assemblers(pd_res), "Marine (common genomes)", "Assemblers - Common marine genomes", METRICS_ASSEMB_L, METRICS_ASSEMB)

    pd_res = pd.read_csv('../assembly/rankings/assemblers_marine_unique.csv', sep='\t')
    tab3 = create_rankings_html(pd_res, format_pd(pd_res), get_source_assemblers(pd_res), "Marine (unique genomes)", "Assemblers - Unique marine genomes", METRICS_ASSEMB_L, METRICS_ASSEMB)

    pd_res = pd.read_csv('../assembly/rankings/assemblers_strain_madness.csv', sep='\t')
    tab4 = create_rankings_html(pd_res, format_pd(pd_res), get_source_assemblers(pd_res), "Strain madness", "Assemblers - Strain madness dataset", METRICS_ASSEMB_L, METRICS_ASSEMB)

    pd_res = pd.read_csv('../assembly/rankings/assemblers_strain_madness_common.csv', sep='\t')
    tab5 = create_rankings_html(pd_res, format_pd(pd_res), get_source_assemblers(pd_res), "Strain madness (common genomes)", "Assemblers - Common strain madness genomes", METRICS_ASSEMB_L, METRICS_ASSEMB)

    pd_res = pd.read_csv('../assembly/rankings/assemblers_strain_madness_unique.csv', sep='\t')
    tab6 = create_rankings_html(pd_res, format_pd(pd_res), get_source_assemblers(pd_res), "Strain madness (unique genomes)", "Assemblers - Unique strain madness genomes", METRICS_ASSEMB_L, METRICS_ASSEMB)

    pd_res, pd_table = read_genome_binning_scores('../binning/genome_binning/marine_dataset/results/amber_marine_nocircular/rankings.tsv')
    tab21 = create_rankings_html(pd_res, pd_table, get_source_genome_binners(pd_res), "Marine", "Genome binners - Marine dataset", METRICS_GBIN_L, METRICS_GBIN)

    tabs_assemblers = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6], css_classes=['bk-tabs-margin'])
    tabs_genome_binners = Tabs(tabs=[tab21], css_classes=['bk-tabs-margin'])

    tabs_main = Tabs(tabs=[Panel(child=tabs_assemblers, title='Assemblers'),
                           Panel(child=tabs_genome_binners, title='Genome binners')])

    html_columns = column(tabs_main, sizing_mode='scale_width', css_classes=['bk-width-auto-main'])
    script, div = components(html_columns)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    html = template.render(js_resources=js_resources,
           css_resources=css_resources,
           script=script,
           div=div)

    with open(os.path.join('../rankings.html'), 'w') as f:
        f.write(html)


if __name__ == "__main__":
    create_html()
