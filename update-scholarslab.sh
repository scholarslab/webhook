#!/bin/bash

REPO_PATH='/var/www/slab/scholarslab.org/repo/'
# need the ending forward slash to copy the contents of this directory, and not create it inside the SITE_PATH location
REPO_SITE='/var/www/slab/scholarslab.org/repo/_site/' 
SITE_PATH='/var/www/slab/scholarslab.org/site/'

cd $REPO_PATH

echo "Grab the latest from GitHub"
git checkout .
git pull

echo "Run rake task to build the site"
# Old user Ruby 2.7.3 updated with system Ruby 3.0.4 but maybe broken in the future...
bundle install
rake publish --trace
#/home/webhooks/.rvm/gems/ruby-2.7.3/wrappers/bundle install
#/home/webhooks/.rvm/gems/ruby-2.7.3/wrappers/rake publish


echo "Copy newly built files to the live site directory"
rsync -avz --inplace --delete --no-times -O -H -X $REPO_SITE $SITE_PATH
