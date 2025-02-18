#!/bin/bash
# set -x
OUTNAME="dbub-fnal"
MAINNAME="main"

files=( "figures/massfit_run56_LH2.pdf" "figures/data_full_xT_syst.pdf" "figures/E906_E866_dbarubar_PDF_model.pdf" "figures/dbub_diff.pdf")
WORK_DIR=`mktemp -d`

for name in ${files[@]}; do
	if [ -e ${name} ]; then
		if [ ${name: -1} == "/" ]; then
			cp -r $name $WORK_DIR
		else
			cp $name $WORK_DIR
		fi
	fi
done
latexpand ${MAINNAME}.tex --expand-bbl build/${MAINNAME}.bbl -o ${WORK_DIR}/${MAINNAME}.tex

tar zcf ${OUTNAME}.tgz -C ${WORK_DIR} .
rm -rf ${WORK_DIR}
