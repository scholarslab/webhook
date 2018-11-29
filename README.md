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
    - `pip install -r requirements`

# Supervisor
Supervisor is a service that keeps Gunicorn running, even with system reboots

## Setup
See the documentation for corgi in the 'server-docs' repo for installing supervisor and config files.

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

# ToDo
- use secret Key for varification
- abstract out for other sites (makergrounds.virginia.edu)
