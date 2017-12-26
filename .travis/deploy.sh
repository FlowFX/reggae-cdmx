#!/bin/sh

# push master branch to production 
git push -f pythonanywhere master
# reload PythonAnywhere web app via the API
python $TRAVIS_BUILD_DIR/.travis/reload-webapp.py
