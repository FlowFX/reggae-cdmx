#!/bin/bash

echo '========================================'
echo '===   Configure remote repository    ==='
echo '========================================'
eval "$(ssh-agent -s)"
git remote add pythonanywhere flowfx@ssh.pythonanywhere.com:/home/flowfx/bare-repos/reggae-cdmx.git
chmod 600 .travis/deploy_key.pem
ssh-add .travis/deploy_key.pem
echo '========================================'
echo '===  Push deploy to PythonAnywhere   ==='
echo '========================================'
git push -f pythonanywhere master
echo '========================================'
echo '===     Reload web app via API       ==='
echo '========================================'
python deploy/reload-webapp.py


# echo '========================================'
# echo '=== Notify Rollbar of new deployment ==='
# echo '========================================'
# curl https://api.rollbar.com/api/1/deploy/ \
# -F access_token=$ROLLBAR_ACCESS_TOKEN \
# -F environment=$ROLLBAR_ENVIRONMENT \
# -F revision=`git log -n 1 --pretty=format:"%H"` \
# -F local_username=`whoami`