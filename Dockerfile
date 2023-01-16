FROM python:3.9

WORKDIR /akash
COPY ./requirements.txt /akash/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /akash/requirements.txt
COPY ./api /akash/api
CMD [ "waitress-serve", "--call", "api.app:create_app"]
EXPOSE 8080