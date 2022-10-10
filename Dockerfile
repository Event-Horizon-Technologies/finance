FROM python:3.10.7
WORKDIR /finance
COPY . .
RUN pip3 install -r requirements.txt