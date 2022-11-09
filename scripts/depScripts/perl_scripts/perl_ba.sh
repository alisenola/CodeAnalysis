#!/bin/bash
#########################################################################################
# 1. Chmod  permission of destination folder to be able to read, write and executable.  #
# 2. Copy all the perl source codes to the destination folder.							#
# 3. Run the contour for each year folder.												#
# 4. Create table and insert table and create dependencies table.   					#
# 5. Generate all the csv output file.													#
# 6. Concat all the csv file into one.													#
# 7. Remove the unwanted string folder info "/media/BIGDATA/"							#
#########################################################################################

#########################################################################################
# 1. chmod permission of your output directory to allow read and write and executable . #
#########################################################################################

output_dir='../../../output_datasets/02_dependency_output/perl/ba'
code_ba='/media/azdata/code/BA_SNAPSHOTS/'
years = '2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013'

# sudo chmod -R 777 $output_dir 
# chmod permission of your output directory to allow read and write and executable 

#####################################################################
# 2. Copy all the perl source codes to the destination folder.      #
#####################################################################

echo "This script will find and copy all perl files from 2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013 with extensions below and into directory that you have specified in this file"

echo "*.fcgi" "*.cgi" "*.pl" "*.pm" "*.plx" "*.perl" "*.px" "*.PL" "*.PM" "*.PLX" "*.PERL" "*.PX" "*.CGI" "*.FCGI"

for i in $years; do 
	echo $output_dir$i 

	sudo find $code_ba$i -name "*.fcgi" -o -name "*.cgi" -o -name "*.pl" -o -name "*.pm" -o -name "*.plx" -o -name "*.perl" -o -name "*.px" -o -name "*.PL" -o -name "*.PM" -o -name "*.PLX" -o -name "*.PERL" -o -name "*.PX" -o -name "*.CGI" -o -name "*.FCGI" | cpio -pdm $output_dir'/perl_files/'$i 
done

#################################################################
# 3. Run the contour for each year folder.						#
#################################################################

echo "This script will run contours for all the years."

echo "Running"
for i in $years; do
	echo $i
	contours --topdir=$output_dir'/perl_files/'$i$code_ba --runid=$i
	mv *.db $output_dir'/dbs/'
done

echo "Done"

#####################################################################
# 4. Create table and insert table and create dependencies table.   #
#####################################################################


for i in $years; do
	echo $i
	sqlite3 $output_dir'/dbs/'$i.db "CREATE TABLE target_file_pkgs (target_file varchar(500),target_pkg varchar(500));"
	sqlite3 $output_dir'/dbs/'$i.db "INSERT INTO target_file_pkgs select distinct source AS target_file, package AS target_pkg from included_module where package in (select distinct [module] from included_module);"
	sqlite3 $output_dir'/dbs/'$i.db "CREATE TABLE dependencies (source_file varchar(500),source_pkg varchar(500),target_file varchar(500),target_pkg varchar(500));"
	sqlite3 $output_dir'/dbs/'$i.db "INSERT INTO dependencies select distinct b.source AS source_file, b.package AS source_pkg, a.target_file, a.target_pkg from target_file_pkgs a JOIN included_module b ON a.target_pkg = b.[module];"
	sqlite3 $output_dir'/dbs/'$i.db "alter TABLE dependencies add column col_year varchar(500)"
	sqlite3 $output_dir'/dbs/'$i.db "update dependencies set col_year='$i';"  
done;


# #####################################################################
# # 5. Generate all the csv output files from the database.			#
# #####################################################################

sqlite3 $output_dir'/dbs/'2002.db <<!
.mode csv
.header off
.out 2002_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!
sqlite3 $output_dir'/dbs/'2003.db <<!
.mode csv
.header off
.out 2003_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!
sqlite3 $output_dir'/dbs/'2004.db <<!
.mode csv
.header off
.out 2004_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!
sqlite3 $output_dir'/dbs/'2005.db <<!
.mode csv
.header off
.out 2005_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!
sqlite3 $output_dir'/dbs/'2006.db <<!
.mode csv
.header off
.out 2006_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!
sqlite3 $output_dir'/dbs/'2007.db <<!
.mode csv
.header off
.out 2007_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!
sqlite3 $output_dir'/dbs/'2008.db <<!
.mode csv
.header off
.out 2007_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!
sqlite3 $output_dir'/dbs/'2009.db <<!
.mode csv
.header off
.out 2007_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!
sqlite3 $output_dir'/dbs/'2010.db <<!
.mode csv
.header off
.out 2007_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!
sqlite3 $output_dir'/dbs/'2011.db <<!
.mode csv
.header off
.out 2007_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!
sqlite3 $output_dir'/dbs/'2012.db <<!
.mode csv
.header off
.out 2007_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!
sqlite3 $output_dir'/dbs/'2013.db <<!
.mode csv
.header off
.out 2007_dep.csv
select col_year,source_file,source_pkg,target_file,target_pkg from dependencies;
.exit
!

mv *.csv $output_dir'/csvs'

#####################################################################
# 6. Concat all the csv file into one.								#
#####################################################################

# concat all the csv into one for BA_SNAPSHOTS data
echo 'cat '$output_dir'/csvs/*.csv > '$output_dir'/csvs/2002_2013_BA.csv'
cat $output_dir'/csvs/'*.csv > $output_dir'/csvs/'2002_2013_BA.csv 


#############################################################################
# 7. Normalize the path string to remove absolue path                       #
# for example: /media/azdata/code/BA_SNAPSHOTS/2000/[relative_path]                 #
# the normalized path will be only the [relative_path]                      #
#############################################################################

sed 's/\/media.*\/BA_SNAPSHOTS\/20[0-9][0-9]\///g' $output_dir'/csvs/2002_2013_BA.csv' > $output_dir'BA_2002_2013_Perl.csv'


