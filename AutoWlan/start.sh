#!/bin/bash
basedir=`cd $(dirname $0); pwd -P`
echo $basedir
cd $basedir
./venv/bin/python login.py xuehao mima --interface xxx --acid 5
