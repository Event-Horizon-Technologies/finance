FROM ubuntu:latest
WORKDIR /finance
COPY . .
RUN apt update 
RUN apt upgrade -y
RUN apt install aptitude -y
RUN aptitude install $(cat requirements.system) -y
RUN pip3 install -r requirements.txt
RUN git config --global --add safe.directory /workspaces/finance
CMD python3 simulator.py 