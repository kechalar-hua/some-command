for i in `ls *.json`;do
  {
  name=${i%%.*}
  python json.py ${name}.json ${name}.json.txt
  } 
done
echo -e 'sample\ttotal_reads\ttotal_bases\tq20_bases\tq30_bases\tq20_rate\tq30_rate\tread1_mean_length\tread2_mean_length\tgc_content' > json.sum.txt
cat *.json.txt >> json.sum.txt
rm -f *.json.txt