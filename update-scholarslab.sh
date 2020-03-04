#!/bin/bash

REPO_PATH='/websites/scholarslab.org/repo'
# need the ending forward slash to copy the contents of this directory, and not create it inside the SITE_PATH location
REPO_SITE='/websites/scholarslab.org/repo/_site/' 
SITE_PATH='/websites/scholarslab.org/site'


cd $REPO_PATH


echo "Grab the latest from GitHub"
git checkout .
git pull

echo "Run rake task to build the site"
/home/webhooks/.rvm/gems/ruby-2.4.1/wrappers/bundle install
/home/webhooks/.rvm/gems/ruby-2.4.1/wrappers/rake publish

echo "Copy newly built files to the live site directory"
rsync -avz --delete --compress --inplace -H -A -X $REPO_SITE $SITE_PATH
