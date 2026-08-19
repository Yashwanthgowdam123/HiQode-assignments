# Assignment 2 - Build Custom Tomcat Image Using Ubuntu

## Objective

Create a custom Docker image by installing Java and Tomcat manually.

---

## Project Structure

```text
assignment2/
├── Dockerfile
└── sample.war
```

---

## Dockerfile

```dockerfile
FROM ubuntu:24.04

LABEL maintainer="Yashwanth Gowda"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        openjdk-21-jdk \
        wget \
        curl \
        tar && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

ENV TOMCAT_VERSION=9.0.112

RUN wget https://archive.apache.org/dist/tomcat/tomcat-9/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz \
    -O /tmp/tomcat.tar.gz && \
    mkdir -p /opt/tomcat && \
    tar -xzf /tmp/tomcat.tar.gz \
    --strip-components=1 \
    -C /opt/tomcat && \
    rm /tmp/tomcat.tar.gz

COPY sample.war /opt/tomcat/webapps/

EXPOSE 8080

CMD ["/opt/tomcat/bin/catalina.sh","run"]
```

---

## Build Image

```bash
docker build -t custom-tomcat:v1 .
```

---

## Run Container

```bash
docker run -d \
--name custom-tomcat-container \
-p 8082:8080 \
custom-tomcat:v1
```

---

## Verify

```bash
docker ps
docker logs custom-tomcat-container
```

---

## Access Application

```
http://<SERVER-IP>:8082/sample/
```

---

## Concepts Learned

- Ubuntu Base Image
- apt-get
- ENV
- JAVA_HOME
- wget
- tar
- Manual Tomcat Installation
- Custom Docker Image
