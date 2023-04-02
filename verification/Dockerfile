FROM python:3-slim
WORKDIR /usr/src/app
COPY common/requirements.txt common/amqp_setup.py common/invokes.py ./
RUN pip install --no-cache-dir -r requirements.txt
COPY verification/verification.py ./
CMD [ "python", "./verification.py" ]