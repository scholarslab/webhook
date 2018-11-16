import os
import git
import subprocess
from flask import Flask, request, abort
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv('SECRET_TOKEN')
path_to_site = "../copy-of-cool-site"
BRANCH = 'master'

app = Flask(__name__)


@app.route('/payload', methods=['POST'])
def webhook():
    if request.method == 'POST':
        if request.json['ref'] == 'refs/heads/' + BRANCH:

            repo = git.Git(path_to_site)
            repo.pull('origin', BRANCH)

            os.chdir(path_to_site)
            subprocess.run(["jekyll", "build"] )

            return 'Got it!', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run()
