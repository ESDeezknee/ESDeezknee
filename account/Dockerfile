FROM python:3-slim
WORKDIR /usr/src/app
COPY common/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY account/account.py ./
CMD [ "python", "./account.py" ]