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
				python src/main/python/partOfSpeech.py train
				python src/main/python/partOfSpeech.py dev
				python src/main/python/partOfSpeech.py test
				;;
             ?)  #当有不认识的选项的时候arg为?
            	echo "unkonw argument"
        esac
done
crf_learn -f 3 -c 1.5 src/main/crf/template target/train.data target/model
crf_test -m target/model target/test.data > result
