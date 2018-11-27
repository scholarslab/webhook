FROM python:3

RUN apt-get update && apt-get install -y git

RUN adduser --disabled-login webhooks

WORKDIR /home/webhooks

COPY requirements.txt /home/webhooks
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

COPY webhooks.py boot.sh /home/webhooks/
RUN chmod +x boot.sh
RUN chown -R webhooks:webhooks /home/webhooks

USER webhooks

EXPOSE 5050

ENTRYPOINT ["/home/webhooks/boot.sh"]
