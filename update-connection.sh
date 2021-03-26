#!/bin/bash

REPO_PATH='/websites/connection.scholarslab.org/repo'
# need the ending forward slash to copy the contents of this directory, and not create it inside the SITE_PATH location
REPO_SITE='/websites/connection.scholarslab.org/repo/_site/' 
SITE_PATH='/websites/connection.scholarslab.org/site'


cd $REPO_PATH


echo "Clear any local changes, then grab the latest from GitHub"
git checkout .
git pull

echo "Run bundle install and bundle exec jekyll build"
/home/webhooks/.rvm/gems/ruby-2.7.2/wrappers/bundle install
/home/webhooks/.rvm/gems/ruby-2.7.2/wrappers/bundle exec jekyll build

echo "Copy newly built files to the live site directory"
rsync -avz --delete --compress --inplace -H -A -X $REPO_SITE $SITE_PATH
