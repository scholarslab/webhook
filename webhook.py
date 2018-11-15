import os
import git
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
            print(request.headers['X-Hub-Signature'])
            repo = git.Git(path_to_site)
            repo.pull('origin', BRANCH)

            return 'Got it!', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run()
