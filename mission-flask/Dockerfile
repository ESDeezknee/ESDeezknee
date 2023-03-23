FROM python:3-slim
WORKDIR /usr/src/app
COPY common/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY mission/mission.py ./
CMD [ "python", "./mission.py" ]