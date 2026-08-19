# Base Image
FROM ubuntu:24.04

# Maintainer
LABEL maintainer="Yashwanth Gowda"

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package index and install required packages
RUN apt-get update && \
    apt-get install -y \
        openjdk-21-jdk \
        wget \
        curl \
        tar && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Java environment
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Tomcat version
ENV TOMCAT_VERSION=9.0.112

# Download and extract Tomcat
RUN wget https://archive.apache.org/dist/tomcat/tomcat-9/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz -O /tmp/tomcat.tar.gz && \
    mkdir -p /opt/tomcat && \
    tar -xzf /tmp/tomcat.tar.gz --strip-components=1 -C /opt/tomcat && \
    rm /tmp/tomcat.tar.gz

# Copy WAR file
COPY sample.war /opt/tomcat/webapps/

# Expose Tomcat port
EXPOSE 8080

# Start Tomcat
CMD ["/opt/tomcat/bin/catalina.sh", "run"]
