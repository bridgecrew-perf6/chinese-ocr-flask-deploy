# base image with python environment
FROM python:3.7-slim-stretch as base
FROM base as builder
# make temp install dir
RUN mkdir /install
WORKDIR /install
# copy python requirements file to base dir
COPY app/requirements.txt /requirements.txt
# install dependency for opencv
RUN apt-get update && apt-get install -y --no-install-recommends libglib2.0-0
# install python environment
RUN pip install --no-cache-dir --prefix="/install" -r /requirements.txt
# multi-stage build
FROM base
COPY --from=builder /install /usr/local
# copy all files needed for the project
COPY /app /app
# assign workdir
WORKDIR /app
# entry point
EXPOSE 5002
CMD [ "python" , "app.py"]