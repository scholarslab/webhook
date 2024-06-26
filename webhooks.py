import os
import git
import subprocess
from flask import Flask, request, abort


application = Flask(__name__)

@application.route('/', methods=['POST'])
def webhooks():
    if request.method == 'POST':
        if request.json['ref'] == 'refs/heads/master':

            subprocess.Popen(["/var/www/slab/webhooks.scholarslab.org/update-scholarslab.sh"])

            return 'Got it!', 202
        else: 
            return 'Not the master branch. Not running the update.', 200
    else:
        abort(400)

@application.route('/connection', methods=['POST'])
def connection():
    if request.method == 'POST':
        if request.json['ref'] == 'refs/heads/master':

            subprocess.Popen(["/var/www/slab/webhooks.scholarslab.org/update-connection.sh"])

            return 'Got it!', 202
        else: 
            return 'Not the master branch. Not running the update.', 200
    else:
        abort(400)

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=5050)
