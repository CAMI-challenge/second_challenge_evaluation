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

METRICS_ASSEMB = {'Sum of scores': 'sum',
                  'Strain recall': 'recall',
                  'Strain precision': 'precision',
                  '# mismatches per 100 kbp': 'mismatches',
                  'Duplication ratio': 'duplication',
                  '# misassemblies': 'misassemblies',
                  'Genome fraction (%)': 'fraction',
                  'NGA50': 'nga50'}

METRICS_GBIN = {'Sum of scores': 'sum',
                'CAMI 1 average completeness (bp)': 'completeness',
                'Average purity (bp)': 'purity',
                'Adjusted Rand index (bp)': 'ari',
                'Percentage of binned bp': 'binnedbp'}

METRICS_TBIN = {'Sum of scores': 'sum',
                'Average completeness': 'completeness',
                'Average purity': 'purity',
                'F1-score': 'f1',
                'Accuracy': 'accuracy'}

METRICS_PROF = {'Sum of scores': 'sum',
                'Completeness': 'completeness',
                'Purity': 'purity',
                'F1 score': 'f1',
                'L1 norm error': 'l1norm',
                'Bray-Curtis distance': 'bcdist',
                'Shannon equitability': 'shannon',
                'Weighted UniFrac error': 'unifrac'}


def get_data_source(pd_res, metrics_dict):
    source_dict = dict(x=pd_res['tool'],
                       top=pd_res['Sum of scores'])
    for k, v in metrics_dict.items():
        source_dict[v] = pd_res[k]
    return ColumnDataSource(source_dict)


def create_rankings_html(pd_res_pd_table, tab_title, title, metrics_dict):
    pd_res, pd_table = pd_res_pd_table
    metrics_list = list(metrics_dict.keys())
    jscript = 'topx[i] = '
    for metric in metrics_list[1:]:
        jscript += "data['" + metrics_dict[metric] + "'][i] * weight_" + metrics_dict[metric] + ".value +"
    jscript = jscript[:-1] + ';'

    source= get_data_source(pd_res, metrics_dict)
    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var topx = data['top'];
        for (let i = 0; i < topx.length; i++) {""" + jscript + """ }
        console.log(data['top'].length);
        source.change.emit();
    """)

    sliders_list = []
    for metric in metrics_list[1:]:
        slider = Slider(start=0, end=20, value=1, step=.5, title=metric + ' weight')
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

    title_div = Div(text=title, style={"width": "1000px", "margin-top": "14px", "font-size": "14pt"})
    if len(sliders_list) > 4:
        return Panel(child=column(title_div, data_table, row(sliders_list[0:4]), row(sliders_list[4:]), p), title=tab_title)
    else:
        return Panel(child=column(title_div, data_table, row(sliders_list), p), title=tab_title)


def read_assemblers_scores(file_path):
    pd_res = pd.read_csv(file_path, sep='\t')
    pd_table = pd_res.set_index('tool').stack().reset_index().rename(columns={'level_1': 'metric', 0: 'value'})

    df_list = []
    for metric, g in pd_table.groupby('metric'):
        x = g.sort_values('value')
        df_list.append(pd.DataFrame({metric: x['tool'].tolist(), 'score' + metric: x['value'].tolist()}))

    return pd_res, pd.concat(df_list, axis=1)


def read_scores(file_path, metrics):
    df_scores = pd.read_csv(file_path, sep='\t', index_col=0)
    df_scores.columns = df_scores.columns.str.replace(r'rank$', '')
    df_scores = df_scores.rename(columns={'sum': 'Sum of scores'})

    df_list = []
    for metric in metrics.keys():
        x = df_scores[metric].str.extract(r'(.*)\s\((\d*)\)$').rename(columns={0: metric, 1: 'score' + metric})
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
                <title>CAMI 2 Challenge software rankings</title>
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
                </style>
            </head>
            <body>
                {{ div }}
                {{ script }}
            </body>
        </html>
        ''')

    assemblers = [('../assembly/rankings/assemblers_marine.csv', "Marine", "Assemblers - Marine dataset"),
                  ('../assembly/rankings/assemblers_marine_common.csv', "Marine (common genomes)", "Assemblers - Common marine genomes"),
                  ('../assembly/rankings/assemblers_marine_unique.csv', "Marine (unique genomes)", "Assemblers - Unique marine genomes"),
                  ('../assembly/rankings/assemblers_strain_madness.csv', "Strain madness", "Assemblers - Strain madness dataset"),
                  ('../assembly/rankings/assemblers_strain_madness_common.csv', "Strain madness (common genomes)", "Assemblers - Common strain madness genomes"),
                  ('../assembly/rankings/assemblers_strain_madness_unique.csv', "Strain madness (unique genomes)", "Assemblers - Unique strain madness genomes")]

    genome_bin = [('../binning/genome_binning/marine_dataset/results/amber_marine_nocircular/rankings.tsv', "Marine GSA", "Genome binners - Marine gold standard assembly"),
                  ('../binning/genome_binning/marine_dataset/results/amber_marine_megahit_nocircular/rankings.tsv', "Marine MEGAHIT", "Genome binners - Marine MEGAHIT assembly"),
                  ('../binning/genome_binning/strain_madness_dataset/results/amber_strain_madness/rankings.tsv', "Strain madness GSA", "Genome binners - Strain madness gold standard assembly"),
                  ('../binning/genome_binning/strain_madness_dataset/results/amber_strain_madness_megahit/rankings.tsv', "Strain madness MEGAHIT", "Genome binners - Strain madness MEGAHIT assembly"),
                  ('../binning/genome_binning/plant_associated_dataset/results/amber_rhizosphere_noplasmids/rankings.tsv', "Plant-associated GSA", "Genome binners - Plant-associated gold standard assembly"),
                  ('../binning/genome_binning/plant_associated_dataset/results/amber_rhizosphere_megahit_noplasmids/rankings.tsv', "Plant-associated MEGAHIT", "Genome binners - Plant-associated MEGAHIT assembly"),
                  ('../binning/genome_binning/plant_associated_dataset/results/amber_rhizosphere_hybrid_noplasmids/rankings.tsv', "Plant-associated hybrid", "Genome binners - Plant-associated hybrid assembly")]

    tax_bin = [('../binning/taxonomic_binning/marine_dataset/data/results/rankings.tsv', 'Marine', 'Taxonomic binners - Marine gold standard assembly (c.), short reads (s.r.), long reads (l.r.)'),
               ('../binning/taxonomic_binning/strain_madness_dataset/data/results/rankings.tsv', 'Strain madness', 'Taxonomic binners - Strain madness gold standard assembly (c.), short reads (s.r.), long reads (l.r.)'),
               ('../binning/taxonomic_binning/plant_associated_dataset/data/results/rankings.tsv', 'Plant-associated', 'Taxonomic binners - Plant-associated gold standard assembly (c.), short reads (s.r.)',)]

    profilers = [('../profiling/marine_dataset/results/OPAL_short_long_noplasmids/rankings.tsv', 'Marine', 'Taxonomic profilers - Marine dataset'),
                 ('../profiling/strain_madness_dataset/results/OPAL_short_long/rankings.tsv', 'Strain madness', 'Taxonomic profilers - Strain madness dataset'),
                 ('../profiling/rhizosphere_dataset/results/OPAL_short_long_noplasmids/rankings.tsv', 'Plant-associated', 'Taxonomic profilers - Plant-associated dataset')]

    panels_assemblers = [create_rankings_html(read_assemblers_scores(x[0]), x[1], x[2], METRICS_ASSEMB) for x in assemblers]
    panels_genome_binners = [create_rankings_html(read_scores(x[0], METRICS_GBIN), x[1], x[2], METRICS_GBIN) for x in genome_bin]
    panels_tax_binners = [create_rankings_html(read_scores(x[0], METRICS_TBIN), x[1], x[2], METRICS_TBIN) for x in tax_bin]
    panels_profilers = [create_rankings_html(read_scores(x[0], METRICS_PROF), x[1], x[2], METRICS_PROF) for x in profilers]

    tabs_assemblers = Tabs(tabs=panels_assemblers, css_classes=['bk-tabs-margin'])
    tabs_genome_binners = Tabs(tabs=panels_genome_binners, css_classes=['bk-tabs-margin'])
    tabs_tax_binners = Tabs(tabs=panels_tax_binners, css_classes=['bk-tabs-margin'])
    tabs_profilers = Tabs(tabs=panels_profilers, css_classes=['bk-tabs-margin'])

    tabs_main = Tabs(tabs=[Panel(child=tabs_assemblers, title='Assemblers'),
                           Panel(child=tabs_genome_binners, title='Genome binners'),
                           Panel(child=tabs_tax_binners, title='Taxonomic binners'),
                           Panel(child=tabs_profilers, title='Taxonomic profilers')])

    title_div = Div(text='CAMI 2 Challenge software rankings', style={"width": "500px", "margin-top": "0px", "font-size": "18pt"})
    html_columns = column(title_div, tabs_main, sizing_mode='scale_width', css_classes=['bk-width-auto-main'])
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
