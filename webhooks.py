import os
import git
import subprocess
from flask import Flask, request, abort

BRANCH = 'master'

application = Flask(__name__)

@application.route('/')
def index():
  return "Webhooks for Scholars' Lab"


@application.route('/payload', methods=['POST'])
def webhooks():
    if request.method == 'POST':
        if request.json['ref'] == 'refs/heads/' + BRANCH:

            subprocess.Popen(["/var/www/webhooks.scholarslab.org/update-scholarslab.sh"])

            return 'Got it!', 202
        else: 
            return 'Not the master branch. Not running the update.', 200
    else:
        abort(400)

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=5050)
