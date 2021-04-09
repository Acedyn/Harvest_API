FROM python

COPY . /opt/harvest_api

RUN pip3 install /opt/harvest_api/

CMD python -m harvest_api -e container
