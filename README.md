# Webhook services

This script is run on corgi, it listens for webhook calls from certain GitHub repos, then runs commands on the server.


This first iteration will get a static copy of ScholarsLab.org on corgi.
```
edit files in a repo 
        ↓
push changes to GitHub repo 
        ↓
webhook on repo sends data to corgi
        ↓
corgi receives data 
        ↓
initiates a git pull from that GitHub repo
        ↓
initiates a jekyll build when pull is done
```
