#
FROM python:3.9
#
COPY . /usr/src/app
#
WORKDIR /usr/src/app
#
RUN pip3 install -r requirements.txt
#
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
