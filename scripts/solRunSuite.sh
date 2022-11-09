#!/bin/bash

#Created 08/23/2016
#ssia@keystonestrategy.com
#Bash script used to run main.py function

#gives it a list of Versions (Ideally never changes for each project)
#Gives it a list of comparisons to perform
#runs the main function, which uses listOfComparisons to call each subsequent function

CKPROJECTPATH="C:/Users/ssia/Documents/GitHub"
CKPROJECTDIR="CrimsonProject"
python3 main.py $CKPROJECTPATH $CKPROJECTDIR
