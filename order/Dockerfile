FROM python:3-slim
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
COPY common/requirements.txt common/invokes.py common/amqp_setup.py ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install Flask[async]
COPY order/order.py ./
CMD [ "python", "./order.py" ]