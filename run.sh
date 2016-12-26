#!/bin/sh
echo "if need preprocessing, use -p.
start running"
while getopts "tp" arg #选项后面的冒号表示该选项需要参数
do
        case $arg in
        	p)
				echo "split the raw data into different dataset-train, dev and test"
				sbt run -Dfile.encoding=utf-8 #使用utf-8编码
				;;
            t)
                echo "tagging the part-of-speech tag"
				python3 src/main/python/partOfSpeech.py train
				python3 src/main/python/partOfSpeech.py dev
				python3 src/main/python/partOfSpeech.py test
				;;
             ?)  #当有不认识的选项的时候arg为?
            	echo "unkonw argument"
        esac
done

for ((f = 1; f <= 10; f = f + 2)) do
	for ((c = 3; c <= 15; c = c + 3))do
		v=f${f}_c${c}
		real_c=$(echo $c 10.0 | awk '{ printf "%0.8f\n" ,$1/$2}')
		echo "f: ${f} c: ${c}" >> log
		crf_learn -f $f -c $real_c src/main/crf/template target/train.data target/model_$v > target/log_$v
		sed '/^iter/d' target/log_$v >> log
		crf_test -m target/model_$v target/dev.data > target/result
		python3 src/main/python/evaluate.py >> log
	done
done
