# Webhook services

This service is run on corgi, it listens for webhook calls from certain GitHub
repos, then runs commands on the server.

## Process
    ```
    you edit files on your laptop
            ↓
    you push changes to the GitHub repo 
            ↓
    a webhook on GitHub sends data to corgi
            ↓
    corgi initiates a `git pull` from that GitHub repo
            ↓
    corgi initiates a command when pull is done
    ```

## Requirements
- python 3.x
- Gunicorn 19.x
- Supervisor 3.x
- Nginx 1.14+
- a user with no login, but shell for setting path ruby 2.4.1 (rvm)

## Server User Setup
A user on the server needs to be set up with .bashrc/.bash_profile/.profile files set to use rvm for the ruby 2.4.1+
- Ask Library IT to create a user.
- Follow a standard tutorial for setting up rvm for the user

# Python Flask app
This set up consists of a Flask app attached to a domain name. The GitHub repo
is set up with a webhook pointing to this domain name/URL.

The Flask app runs a `git pull` which pulls down the latest files from the
GitHub repo that was just updated. Then the app runs a command to build the
static files (or whatever else is required).

## Files
- webhooks.py: the main application. Does the commands when the URL is requested.
- requirements.txt: all the modules needed by the app to run

## Setup
Just clone this repo into a directory and that's it.


# Gunicorn
Gunicorn is used to provide the layer/connection between the Flask app and Nginx

- Make sure the gunicorn script in .venv/bin/gunicorn is executable by the
  webhooks user.

## Setup
Gunicorn should be installed using a python virtual environment.
- Follow instructions like this to install python36u from the ius yum repo
    - https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-centos-7
- change to the Flask app directory
    - Create a virtual environment in the Flask app directory
    - `python3.6 -m venv .venv` (the .venv can be any name)
- Activate the virtual environment
    - `source .venv/bin/activate`
- Install modules
    - `pip install -r requirements.txt`

# Supervisor
Supervisor is a service that keeps Gunicorn running, even with system reboots

## Setup
See the documentation for corgi in Confluence for installing supervisor and config files.

- create a program config file at /etc/supervisord.d/webhooks.config
- 
    ```
      [program:webhooks]
    directory=/var/www/webhooks.scholarslab.org
    chdir=/var/www/webhooks.scholarslab.org
    command=/var/www/webhooks.scholarslab.org/.venv/bin/gunicorn --log-level debug --bind 127.0.0.1:5050 webhooks:application --error-logfile '-' --timeout 240 --workers 1
    user=webhooks
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/supervisor/webhooks.scholarslab.org.err.log
    stdout_logfile=/var/log/supervisor/webhooks.scholarslab.org.out.log
    log_stderr=true
    logfile=/var/log/supervisor/webhooks.scholarslab.org.log
    redirect_sterr=True
    ```

# Nginx
Nginx is the reverse proxy. It takes the initial request for the domain name, then passes it to Gunicorn.

## Setup
Install with yum. 

# Adding a new website
- Log in to corgi and change to the /var/www/webhooks.scholarslab.org/ folder.
- Create a new update script (copy update-scholarslab.sh), and edit as
  appropriate (the path variables, ruby version, and bundle/jekyll commands)
- Create the directories needed in /websites/ folder
  - Make a '/websites/newdomain.org/' folder with 'repo' and 'site' subfolders
  -  `mkdir /websites/newdomain.org/{repo,site}`
- clone the repo (and the correct branch) into the correct folder (see update
  script, usually the 'repo' folder)
- Update the webhooks.py file. 
  - Create a new route specific for the new site (change BRANCH, DOMAIN_NAME,
    and domain_name in the example below)
  - Examples like: 
    - DOMAIN_NAME = a one word description or part of the domain name,
      awesome-site.org could be just 'awesome'. It must be unique from the other
      routes.
    - BRANCH = main, master, the-best
    - domain_name = can be same as DOMAIN_NAME or the FQDN, 'update-awesome-site.org.sh'
  ```
  @application.route('/DOMAIN_NAME', methods=['POST'])
  def DOMIN_NAME():
      if request.method == 'POST':
          if request.json['ref'] == 'refs/heads/BRANCH':

              subprocess.Popen(["/var/www/webhooks.scholarslab.org/update-domain_name.sh"])

              return 'Got it!', 202
          else: 
              return 'Not the master branch. Not running the update.', 200
      else:
          abort(400)
  ```
- Create a new nginx config file
  - Make a new file at `/etc/nginx/conf.d/domain.name.here.org.conf`
  ```
  server {
  listen 80;
  server_name domain.name.here.org;

  root /websites/domain.name.here.org;
  index index.html;

  access_log /var/log/nginx/domain.name.here.org_access.log;
  error_log /var/log/nginx/domain.name.here.org_error.log;

  }
  ```
- Test and reload Nginx
  - `sudo service nginx configtest` To double check everything is good.
  - `sudo service nginx reload`
- Once all changes are made and tested by hand to work (run the update script
  manually), then restart supervisord
  - `sudo supervisorctl restart webhooks`
- Change the DNS to point to corgi (128.143.228.220)
- Back on corgi, run certbot to generate the SSL certs
  - `sudo certbot-auto --nginx`
- Add the webhook to the GitHub repo. On the GitHub webiste, go to the repo,
  then Settings->Webhooks->Add webhook button.
  - Payload URL = http://webhooks.scholarslab.org/DOMAIN_NAME (DOMAIN_NAME is
    the same as what you used in the webhooks.py file for the route name)
  - Content Type = application/json
  - No secret yet
  - Just the push event
  - Active box checked

# ToDo
- use secret Key for varification
