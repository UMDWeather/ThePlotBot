#!/bin/bash
# animate satellite imagery for website
# C. Martin - 9/2016

sats="GOES-13
	GOES-15
	"
prods="IR
	VIS
	13.3
	WV
	3.9
	"
doms="00
	01
	02
	"

satdir=/var/www/html/products/sat
animdir=/var/www/html/recent/anim
for s in $sats; do
 for p in $prods; do
  for d in $doms; do
   # past 3 hours
   end="$p"_$d.png
   match=$satdir/$s/*_$end
   images=`find $match -type f -mmin -180`
   last=`find $match -type f -mmin -180 | tail -n 1`
   out=$animdir/3hr_"$s"_"$p"_"$d".gif
   convert -delay 10 -loop 0 $images -delay 200 $last $out
  done
 done
done
