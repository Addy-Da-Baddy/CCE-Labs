#!/bin/bash
echo "Enter the name of a file or directory"
read filename
if [ -z $filename ]; then
	echo "Please enter the name" 
elif [ -f $filename ]  ; then
	echo "$filename is a file"
elif [ -d $filename ]; then
	echo "$filename is a directory"
else 
	echo "$filename is neither a file nor directory or no element with such a name was found"
fi

#use testdir and testtext to test

