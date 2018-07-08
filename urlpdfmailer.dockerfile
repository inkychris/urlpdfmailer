FROM ubuntu:18.04

WORKDIR /usr/src/urlpdfmailer
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    tzdata

RUN ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime \
 && dpkg-reconfigure -f noninteractive tzdata

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY urlpdfmailer ./urlpdfmailer
COPY main.py logging_config.yml ./

COPY settings.yml ./

ENTRYPOINT ["python3", "main.py", "settings.yml"]
