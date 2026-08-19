FROM ubuntu:24.04

LABEL maintainer="Yashwanth Gowda"

ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
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

# Java Environment
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Tomcat Version
ENV TOMCAT_VERSION=9.0.112

# Download Tomcat
RUN wget https://archive.apache.org/dist/tomcat/tomcat-9/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz \
    -O /tmp/tomcat.tar.gz && \
    mkdir -p /opt/tomcat && \
    tar -xzf /tmp/tomcat.tar.gz \
    --strip-components=1 \
    -C /opt/tomcat && \
    rm /tmp/tomcat.tar.gz

# Clone source code
RUN git clone --depth 1 https://github.com/Siddeshg672/hello_world_public_war.git /app

# Build WAR
WORKDIR /app

RUN mvn clean package

# Copy WAR to Tomcat
#RUN cp target/*.war /opt/tomcat/webapps/webapp.war
#RUN ls -l target
#RUN find /app -name "*.war" -o -name "pom.xml"
RUN cp /app/webapp/target/webapp.war /opt/tomcat/webapps/webapp.war

EXPOSE 8080

CMD ["/opt/tomcat/bin/catalina.sh","run"]
