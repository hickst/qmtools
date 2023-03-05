FROM python:3.11.2

LABEL maintainer="Tom Hicks hickst@arizona.edu"

ARG TESTS=src/notests

ENV RUNNING_IN_CONTAINER True
ENV INSTALL_PATH /qmtools

# create mount points inside container
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY setup.py setup.py
COPY .bash_env /etc/trhenv
COPY src src
COPY $TESTS $TESTS

# Run setup.py to build & install packages and CLI scripts:
RUN pip install .

ENTRYPOINT [ "run_traffic" ]
CMD [ "-v", "-h" ]
