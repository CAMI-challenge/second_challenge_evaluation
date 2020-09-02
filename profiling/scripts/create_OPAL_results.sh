#!/usr/bin/env bash
set -e  # exit on error
set -u  # exit on undefined variable
#set -x  # tracing on

# Set magic variables for current file & dir (credit: https://kvz.io/bash-best-practices.html)
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
__base="$(basename ${__file} .sh)"
__root="$(cd "$(dirname "${__dir}")" && pwd)"


# initial test for creating the figures using OPAL
opalScript=/home/dkoslicki/Desktop/OPAL/opal.py  # FIXME: not portable
pythonExec=/home/dkoslicki/anaconda3/envs/OPAL/bin/python  # FIXME: not portable

# get tool names, version, and anonymous names into arrays
IFS=$'\r\n' GLOBIGNORE='*' command eval  'toolNames=($(<tools.txt))'
IFS=$'\r\n' GLOBIGNORE='*' command eval  'versions=($(<versions.txt))'
IFS=$'\r\n' GLOBIGNORE='*' command eval  'anonymousNames=($(<anonymous_names.txt))'

# Marine short
marineBase=${__root}/marine_dataset/
groundTruth=${marineBase}/data/ground_truth/gs_marine_short.profile
## default args
opalOut=${marineBase}/results/OPAL_default
label="Marine Dataset, short & long reads"

# Look for results to evaluate
toEval=()
labels=()
i=0
for anonymousName in "${anonymousNames[@]}"
do
  fileName=$(find ${marineBase} -name ${anonymousName}.profile)
  if test -f "${fileName}"; then
    #toEval+=( "$(find ${marineBase} -name ${anonymousName}.profile" )
    toEval+=( "${fileName}")
    labels+=( "${toolNames[i]}_${versions[i]}" )
  fi
  i=$((i+1))
done

echo $toEval
echo $labels

# Delete results if they exist
if [ -d "${opalOut}" ]
then
  rm -r "${opalOut}"
fi

# Run OPAL
: << 'END'
${pythonExec} ${opalScript} -g "${groundTruth}" \
-o "${opalOut}" \
-d "${label}" \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/A_1.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/B_1.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/C_4.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/D_1.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/E_1.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/F_1.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/G_1.profile \
-l "A,B,C,D,E,F,G"


# Then Filter
opalOut=/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/output_filtered_1/
/home/dkoslicki/anaconda3/envs/OPAL/bin/python $opalScript -g $groundTruth \
-o $opalOut \
-d "Marine Dataset, short & long reads" \
--metrics_plot_abs c,p,b \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/A_1.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/B_1.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/C_4.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/D_1.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/E_1.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/F_1.profile \
/home/dkoslicki/Desktop/OPAL/EMDUnifracTest/data/G_1.profile \
-l "A,B,C,D,E,F,G" -f 1 -b 'lambda x: 1/float(x)'
END
