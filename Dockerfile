FROM python 
WORKDIR /finance
COPY . .
RUN apt update 
RUN apt upgrade -y
RUN pip3 install -r requirements.txt