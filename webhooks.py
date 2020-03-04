import os
import git
import subprocess
from flask import Flask, request, abort

path_to_site = "/var/www/scholarslab.org"
BRANCH = 'master'

application = Flask(__name__)

@application.route('/')
def index():
  return "Webhooks for Scholars' Lab"


@application.route('/payload', methods=['POST'])
def webhooks():
    if request.method == 'POST':
        if request.json['ref'] == 'refs/heads/' + BRANCH:

            repo = git.Git(path_to_site)
            repo.pull('origin', BRANCH)

            os.chdir(path_to_site)
            subprocess.run(["/home/webhooks/.rvm/gems/ruby-2.4.1/wrappers/rake", "publish"])

            return 'Got it!', 200
    else:
        abort(400)

if __name__ == '__main__':
    application.run(debug=True, host='127.0.0.1', port=5050)
