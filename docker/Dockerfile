FROM python:3.6

RUN pip3 install --process-dependency-links git+https://github.com/thperret/m2mb#egg=m2mb

EXPOSE 25

ENV WEBHOOK_URL ""

ADD docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["bash", "/docker-entrypoint.sh"]
