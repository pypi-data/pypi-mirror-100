while getopts q:a:l:o:x: flag
do
    case "${flag}" in
	q) query_dir=${OPTARG};;
	a) accessory_dir=${OPTARG};;
  l) aligned=${OPTARG};;
  o) out_dir=${OPTARG};;
  x) cores=${OPTARG};;
    esac
done
out_dir=${out_dir}/depp_results
echo "aligning sequences..."
if [ -z "${aligned+x}" ]
then
  for f in ${query_dir}/*.fa; do
    # $1 gene
    # $2 accessory_dir
    # $3 query_dir
    # $4 out_dir
    f=$(basename -- "$f")
    f="${f%.*}"
#    echo $f
    run_upp.sh ${f} ${accessory_dir} ${query_dir} ${cores} > /dev/null 2>&1 &
  done
  wait
fi
echo "finish alignment!"
echo "calculating distance matrices..."
if [ -z "${aligned+x}" ]
then
  for f in ${query_dir}/*aligned.fa; do
    f=$(basename -- "$f")
    f="${f%_*}"
    distance_depp.sh -q ${query_dir}/${f}_aligned.fa -b ${accessory_dir}/${f}.fa -m ${accessory_dir}/${f}.ckpt -t ${accessory_dir}/wol.nwk -o ${out_dir}/${f} > /dev/null 2>&1 &
  done
  wait
else
  for f in ${query_dir}/*.fa; do
    f=$(basename -- "$f")
    f="${f%.*}"
    distance_depp.sh -q ${query_dir}/${f}.fa -b ${accessory_dir}/${f}.fa -m ${accessory_dir}/${f}.ckpt -t ${accessory_dir}/wol.nwk -o ${out_dir}/${f} > /dev/null 2>&1 &
  done
  wait
fi
agg_dist.py -o ${out_dir} -a ${accessory_dir}
echo "finish distance matrices!"
echo "placing queries..."
run_apples.py -d ${out_dir}/summary/summarized_dist.csv -t ${accessory_dir}/wol.nwk -o ${out_dir}/summary/placement.jplace -f 0.25 -b 25
gappa examine graft --jplace-path ${out_dir}/summary/placement.jplace --out-dir ${out_dir}/summary/ --allow-file-overwriting > /dev/null 2>&1
echo "finish queries placement!"