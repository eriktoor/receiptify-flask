# FROM ubuntu:20.04 # 430 mb 
FROM python:3.9-alpine

# Create app directory
WORKDIR .

COPY . .

RUN python setup.py install

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]