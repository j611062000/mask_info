FROM python

RUN apt-get update -y && \
    apt-get install -y python-pip cron

WORKDIR /app

COPY Config/config.yaml /etc/config.yaml
COPY util.py /apt/util.py

RUN mkdir -p /app/templates

COPY bin /apt/bin
COPY cron/crontab /etc/cron.d/update_mask_info
RUN chmod 0644 /etc/cron.d/update_mask_info
RUN crontab /etc/cron.d/update_mask_info
RUN touch /var/log/cron.log

COPY app/app.py /app/app.py
RUN pip install Flask requests Pyaml

CMD sh /apt/bin/init.sh