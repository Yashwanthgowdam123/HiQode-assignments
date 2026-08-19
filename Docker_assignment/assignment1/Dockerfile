# Use the official Tomcat image as the base image
FROM tomcat:8-jre8-alpine

# Maintainer information (optional)
LABEL maintainer="Yashwanth Gowda"

# Copy the WAR file into Tomcat's deployment directory
COPY sample.war /usr/local/tomcat/webapps/

# Expose Tomcat's default HTTP port
EXPOSE 8080

# Start the Tomcat server
CMD ["catalina.sh", "run"]
