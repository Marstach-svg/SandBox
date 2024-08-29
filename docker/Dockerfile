FROM python:3.11.3-buster

ARG project_dir=/project/

ADD ./requirements.txt $project_dir

WORKDIR $project_dir

RUN pip install -r requirements.txt
