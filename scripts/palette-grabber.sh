#!/bin/bash

#location to find the images
LOC="/home/goatslayer/Desktop/working/cinema-palettes/working"

# http://graphicdesign.stackexchange.com/a/82105
# {'Name':['e91c26','3c816e','dd8752','972220','8ba387','b79193']},

#command to get hex values from image magick and only output
#the hex...where normal output is a more complex table...
#echo -E $(convert $file -depth 8 txt:- | sed -e "1d;s/.* #/#/;s/ .*//" | sort -u)"]},"

python_palette_maker ()
{
	printf "{'"
	printf $(basename $file) | sed -E s/.png// 
	printf "':["
	echo -E $(convert $file -depth 8 txt:- | sed -e "1d;s/.* #/#/;s/ .*//" | sort -u)"]},"
}

# Find loop...
oIFS=$IFS
IFS=$'\n'

find "$LOC"/*.png -type f | while read -r file; do
   python_palette_maker "$file"
done

IFS=$oIFS
