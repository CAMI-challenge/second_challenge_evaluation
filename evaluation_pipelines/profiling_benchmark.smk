from os import path

submission_dir = '/net/sgi/cami/cami2_extract/users'
gold_standards = {'marmgCAMI2_short_read': '/net/sgi/metagenomics/cami2_benchmark/gold_standard/profiling/taxonomic_profile_marine_short.profile',
                  'strmgCAMI2_short_read': '/net/sgi/metagenomics/cami2_benchmark/gold_standard/profiling/taxonomic_profile_strain_madness_short.new.profile'}

# taxonomic_profile_strain_madness_short.new.profile

outdir = '../outputs/evaluation'
#user, submission, method = glob_wildcards(submission_dir + '/{userid}/profiling/{submissionid}/data/{method}.profile')


all_submissions, = glob_wildcards(submission_dir + '/{submission}.profile')
# print(samples)

profile_goldstandard_dict = {}
submissions = []

for profile in all_submissions:
    with open(submission_dir + '/' + profile + '.profile', 'r') as fh:
        for line in fh:
            line = line.strip()
            if line.startswith('@SampleID:'):
                sample = line.split(':')[1].strip()
                break
        if sample.startswith('marmgCAMI2_short_read'):
            profile_goldstandard_dict[profile] = 'marmgCAMI2_short_read'
            submissions.append(profile)
        elif sample.startswith('strmgCAMI2_short_read'):
            profile_goldstandard_dict[profile] = 'strmgCAMI2_short_read'
            submissions.append(profile)
        else:
            continue



# def get_goldstandard(wc):
#     with open(submission_dir + '/' + wc.submission, + '.profile', 'r') as fh:
#         for line in fh:
#             line = line.strip()
#             if line.startswith('@SampleID:'):
#                 sample = line[11:]
#                 break
#         if sample.startswith('marmgCAMI2_short_read'):

#             return gold_standards['marmgCAMI2_short_read']
#         # or strmgCAMI2_short_read
#         else:
#             return gold_standards['strmgCAMI2_short_read']


rule all:
    input:
        expand(outdir + '/{submission}/results.tsv', submission=submissions)


rule opal:
    input:
        profile = path.join(submission_dir, '{submission}.profile'),
        gold_standard = lambda wc: gold_standards[profile_goldstandard_dict[wc.submission]]
    output:
        outdir + '/{submission}/results.tsv'
    params:
        output_dir = outdir + '/{submission}',
        label = lambda wc: wc.submission.split('/')[-1]
    shell:
        """
        opal.py -g {input.gold_standard} {input.profile} -l "{params.label}" -o {params.output_dir}
        """
