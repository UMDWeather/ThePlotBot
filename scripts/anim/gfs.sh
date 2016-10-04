#!/bin/bash
# animate some GFS output for website
# C. Martin - 9/2016

gfsdir=/var/www/html/products/grib2/GFS
animdir=/var/www/html/recent/anim

prods="t2
	lvl_500vorticity
        "
doms="d01
        d02
        "

# get most recent GFS plots
lastgfs=`ls -rt "$gfsdir" | tail -1`

for p in $prods; do
 for d in $doms; do
  end=_$d.png
  match=$gfsdir/$lastgfs/$p*$end
  images=`find $match -type f -mmin -360`
  last=`find $match -type f -mmin -360 | tail -n 1`
  out=$animdir/GFS_"$p"_"$d".gif
  convert -delay 50 -loop 0 $images -delay 200 $last $out
 done
done
