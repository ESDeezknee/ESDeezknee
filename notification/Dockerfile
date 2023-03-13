FROM python:3-slim
WORKDIR /usr/src/app
COPY notification/requirements.txt common/amqp_setup.py ./
RUN pip install --no-cache-dir -r requirements.txt
COPY notification/notification.py  ./
CMD [ "python", "./notification.py" ]