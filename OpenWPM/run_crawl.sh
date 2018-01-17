#!/bin/bash

echo "Run the code"
start=247
end=247

echo "We start with domain id $start and ends with domain id $end."
for (( i=$start;i<=$end;i++ ));
do
     echo $i
     python crawl_ke.py $i |& tee ./logs/"$i.domain.log"
     wait
     echo "oOzzzZZZ"
     sleep 10
done

#rm -rf /tmp/*