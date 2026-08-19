# Assignment 3 - Clone Source from GitHub and Build Automatically

## Objective

Clone a Maven project from GitHub, build the WAR file using Maven, deploy it into Tomcat, and run the application.

---

## Project Structure

```text
assignment3/
└── Dockerfile
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
        maven \
        git \
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

RUN git clone --depth 1 https://github.com/Siddeshg672/hello_world_public_war.git /app

WORKDIR /app/webapp

RUN mvn clean package

RUN cp /app/webapp/target/webapp.war /opt/tomcat/webapps/webapp.war

EXPOSE 8080

CMD ["/opt/tomcat/bin/catalina.sh","run"]
```

---

## Build Image

```bash
docker build --progress=plain -t github-webapp:v1 .
```

---

## Run Container

```bash
docker run -d \
--name github-webapp-container \
-p 8083:8080 \
github-webapp:v1
```

---

## Verify

```bash
docker ps
docker logs github-webapp-container
```

---

## Access Application

```
http://<SERVER-IP>:8083/webapp/
```

---

## Issues Faced

### 1. Incorrect GitHub Repository URL

**Issue**

Repository cloning failed.

**Resolution**

Updated the repository URL to the correct GitHub repository.

---

### 2. Incorrect WAR File Path

**Issue**

Docker build failed while copying the WAR file.

```
cp target/*.war: No such file or directory
```

**Resolution**

Identified the generated WAR file location and updated the Dockerfile.

```dockerfile
RUN cp /app/webapp/target/webapp.war /opt/tomcat/webapps/webapp.war
```

---

### 3. Incorrect Working Directory

**Issue**

Maven was executed from the wrong directory.

**Resolution**

Changed the working directory.

```dockerfile
WORKDIR /app/webapp
```

---

## Concepts Learned

- Git Clone inside Docker
- Maven Build inside Docker
- WORKDIR
- Multi-step Docker Build
- Java Environment Variables
- Apache Tomcat Deployment
- Docker Build Process
- Docker Layer Caching
- Containerized Java Application Deployment

---

# Docker Commands Used

```bash
docker pull
docker build
docker run
docker ps
docker ps -a
docker images
docker logs
docker exec
docker inspect
docker stop
docker start
docker restart
docker rm
docker rmi
```

---

# Learning Outcome

After completing these assignments, you will understand:

- Docker Fundamentals
- Docker Images and Containers
- Dockerfile Instructions
- Java Application Deployment
- Apache Tomcat Deployment
- Building Docker Images
- Running Containers
- Deploying WAR Files
- Git Integration
- Maven Integration
- Ubuntu-based Docker Images
- Official vs Custom Docker Images
- End-to-End Java Web Application Deployment
