# Docker Assignments

This repository contains solutions for Docker assignments focused on deploying Java web applications using Apache Tomcat.

---

# Assignment 1

## Objective

Create a Docker image using the official Tomcat image and deploy a Java web application (WAR file).

### Requirements

- Create a Maven Web Application.
- Build the project to generate a WAR file.
- Create a Dockerfile using the official Tomcat image.
- Copy the generated WAR file into Tomcat's `webapps` directory.
- Build the Docker image.
- Run the Docker container.
- Verify that the application is accessible through the browser.

---

# Assignment 2

## Objective

Create a custom Docker image by manually installing Apache Tomcat on Ubuntu and deploy a Java web application.

### Requirements

- Use Ubuntu as the base image.
- Install Java (JDK).
- Download and extract Apache Tomcat.
- Configure Java environment variables.
- Copy the WAR file into Tomcat's deployment directory.
- Build the Docker image.
- Run the Docker container.
- Verify that the application is accessible.

---

# Assignment 3

## Objective

Build and deploy a Java web application directly from its GitHub source repository.

### Requirements

- Use Ubuntu as the base image.
- Install Java, Maven, Git, wget, curl, and tar.
- Download and configure Apache Tomcat.
- Clone the application source code from GitHub.
- Build the application using Maven.
- Generate the WAR file.
- Copy the generated WAR into Tomcat's `webapps` directory.
- Build the Docker image.
- Run the Docker container.
- Verify that the application is successfully deployed and accessible.

---

## Expected Learning Outcomes

After completing these assignments, you should be able to:

- Understand Docker fundamentals.
- Write Dockerfiles.
- Build Docker images.
- Run Docker containers.
- Deploy Java WAR applications on Apache Tomcat.
- Build custom Docker images using Ubuntu.
- Automate application builds using Git and Maven inside Docker.
- Understand the complete Docker image build and deployment workflow.
