#!/bin/sh

# start ssh agent
eval "$(ssh-agent -s)"
chmod 600 deploy_key
ssh-add deploy_key
# configure remote repository
git remote add pythonanywhere flowfx@ssh.pythonanywhere.com:/home/flowfx/bare-repos/reggae-cdmx.git
# push master branch to production 
git push -f pythonanywhere master
