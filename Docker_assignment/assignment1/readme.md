# Assignment 1 - Deploy WAR Using Official Tomcat Image

## Objective

Deploy a Maven-generated WAR file using the official Tomcat Docker image.

---

## Prerequisites

- Docker
- Java 21
- Maven 3.8+
- Ubuntu

---

## Project Structure

```text
assignment1/
├── Dockerfile
└── sample.war
```

---

## Build Maven Project

```bash
mvn clean package
```

Generated artifact:

```text
target/sample.war
```

---

## Dockerfile

```dockerfile
FROM tomcat:8-jre8-alpine

LABEL maintainer="Yashwanth Gowda"

COPY sample.war /usr/local/tomcat/webapps/

EXPOSE 8080

CMD ["catalina.sh","run"]
```

---

## Build Docker Image

```bash
docker build -t sample-webapp:v1 .
```

---

## Run Container

```bash
docker run -d \
--name sample-webapp \
-p 8081:8080 \
sample-webapp:v1
```

---

## Verify

```bash
docker ps
docker logs sample-webapp
```

---

## Access Application

```
http://<SERVER-IP>:8081/sample/
```

---

## Concepts Learned

- Docker Image
- Docker Container
- Dockerfile
- FROM
- COPY
- EXPOSE
- CMD
- Official Images
- Tomcat Auto Deployment

---
