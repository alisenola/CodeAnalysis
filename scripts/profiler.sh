#!/bin/sh

#Created 09/21/2016
#ssia@keystonestrategy.com
#General bash script for profiling


#count of all files within directory
find . -type f | wc -l

#Count of all file extensions within directory
find . -type f | sed 's/.*\.//' | sort | uniq -c
	
#Count of files per subdirectory
for f in *; do [ -d ./"$f" ] && find ./"$f" -type f -exec echo \; | wc -l && echo $f; done

#Count of file extensions per subdirectory
for f in *; do [ -d ./"$f" ] && echo FolderName : "$f";
[ -d ./"$f" ] && find ./"$f" -type f | perl -ne 'print $1 if m/\.([^.\/]+)$/' | sort -u; done

find . -type f -name '*' | xargs wc -l

#sloccount
sloccount .