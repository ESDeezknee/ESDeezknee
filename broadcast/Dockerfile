FROM python:3-slim
WORKDIR /usr/src/app
COPY common/requirements.txt common/invokes.py ./
RUN pip install --no-cache-dir -r requirements.txt
COPY  broadcast/broadcast.py ./
CMD [ "python", "./broadcast.py" ]