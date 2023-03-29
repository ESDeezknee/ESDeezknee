FROM python:3-slim
WORKDIR /usr/src/app
COPY common/requirements.txt common/invokes.py common/amqp_setup.py ./
RUN pip install --no-cache-dir -r requirements.txt
COPY queueticket/queueticket.py  ./
CMD [ "python", "./queueticket.py" ]
