FROM python
WORKDIR /finance
COPY . .
RUN pip3 install -r requirements.txt
CMD python3 simulator.py
