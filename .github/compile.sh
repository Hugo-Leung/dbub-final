current_tag=$1
prev_tag=$2

MAIN="main"
latex_option=""
outName=""
if [[ "${current_tag}" =~ refs/tags/* ]]
then
	outName="dbub_${current_tag:10}"
else
	outName="dbub_${current_tag}"
fi

latexmk ${latex_option} -outdir=build ${MAIN}

if [ -n "${prev_tag}" ]; then
	latexdiff-vc --git -r ${prev_tag} ${MAIN}.tex  --flatten
	diffName=${MAIN}-diff${prev_tag}
	echo ${diffName}
	latexmk ${latex_option} -outdir=build ${diffName}
fi

if [ -n "${outName}" ]; then
	mv build/${MAIN}.pdf build/$outName.pdf
fi
