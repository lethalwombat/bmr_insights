# python base image
FROM python:3.8-slim-buster
USER root

# working directory
WORKDIR /app

# update runtime packages
RUN \ 
    apt-get update && \ 
    apt-get install -y

# copy requirements.txt into the container
COPY requirements.txt requirements.txt

# upgrade pip and setuptools
RUN \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

# copy applications assets into the container
COPY app.py app.py
COPY helpers.py helpers.py

# expose 8050 to the outside world
EXPOSE 8051

# entrypoint to the application
CMD ["python", "app.py"]
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:server"]
