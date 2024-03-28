FROM ubuntu:22.04

RUN apt update
RUN apt install -y python3-pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /claimrx

WORKDIR /claimrx/

ENV PORT 8000
EXPOSE 8000

CMD exec uvicorn appserver.main:app --host 0.0.0.0