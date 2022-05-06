#!/bin/bash  
## git upload auto script - example script
## CLASS_PROGRAMMING 
## command line param, example for a repo:   $1 => username/username.github.io.git

PATH_REPO=ShihabYasin/shihabyasin.github.io

git remote set-url origin git@github.com:$PATH_REPO

#cd $PATH_REPO
git add .

currentDate=`date +"%Y-%m-%d %T"`
git commit -m  currentDate
git pull origin gh-pages
git push origin gh-pages

exit 1
