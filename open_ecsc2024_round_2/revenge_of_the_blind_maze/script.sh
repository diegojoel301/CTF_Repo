#!/bin/bash

for mov in $(cat movs)
do
  
  curl -s "http://blindmazerevenge.challs.open.ecsc2024.it/maze?direction=$mov" -H "Cookie: session=dV6Iyt5K89iD23ArIFg49t_ACnpXueU4r-q3dQSiJ3k" | grep -i "openECSC"&

done
