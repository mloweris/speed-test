FROM ubuntu:18.10

RUN apt update
RUN apt install -y python3-pip


ADD requirements.txt /

RUN pip3 install -r requirements.txt

ADD test.py /

CMD [ "python3", "./test.py" ]


