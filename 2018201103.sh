#!/bin/bash

#Implemented in python2.7

argc="$#" 

if [ $argc -eq 1 ]
then
    python2 2018201103_2.py "$1"
else
    python2 2018201103_1.py "$1" "$2"
fi
