#!/bin/sh

# push master branch to production 
cd $TRAVIS_BUILD_DIR
git push -f pythonanywhere master
