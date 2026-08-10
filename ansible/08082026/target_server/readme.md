# Tomcat Deployment using Ansible - Lab Setup (Version 1)

## Objective

Prepare a Tomcat server with a Java web application (Version 1) that will later be updated using Ansible deployment.

---

# Environment

| Component | Details |
|-----------|---------|
| OS | Ubuntu |
| Java | OpenJDK 17 |
| Tomcat | Apache Tomcat 10 (Binary Installation) |
| Maven | Apache Maven 3.6.3 |
| Installation Path | /opt/tomcat |

---

# Step 1 - Install Java

```bash
sudo apt update
sudo apt install openjdk-17-jdk -y
```

Verify:

```bash
java -version
```

---

# Step 2 - Install Maven

```bash
sudo apt install maven -y
```

Verify:

```bash
mvn -version
```

---

# Step 3 - Create Tomcat User

```bash
sudo groupadd tomcat
sudo useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat
```

---

# Step 4 - Download Apache Tomcat

```bash
cd /tmp

wget https://downloads.apache.org/tomcat/tomcat-10/v10.1.42/bin/apache-tomcat-10.1.42.tar.gz
```

---

# Step 5 - Install Tomcat

```bash
sudo mkdir -p /opt/tomcat

sudo tar -xzf apache-tomcat-10.1.42.tar.gz \
-C /opt/tomcat --strip-components=1
```

---

# Step 6 - Set Ownership

```bash
sudo chown -R tomcat:tomcat /opt/tomcat

sudo chmod +x /opt/tomcat/bin/*.sh
```

---

# Step 7 - Configure Tomcat Service

Create:

```bash
sudo vim /etc/systemd/system/tomcat.service
```

Contents:

```ini
[Unit]
Description=Apache Tomcat Web Application Container
After=network.target

[Service]
Type=forking

User=tomcat
Group=tomcat

Environment="JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64"
Environment="CATALINA_HOME=/opt/tomcat"
Environment="CATALINA_BASE=/opt/tomcat"
Environment="CATALINA_PID=/opt/tomcat/temp/tomcat.pid"

ExecStart=/opt/tomcat/bin/catalina.sh start
ExecStop=/opt/tomcat/bin/catalina.sh stop

Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable service:

```bash
sudo systemctl enable tomcat
```

Start Tomcat:

```bash
sudo systemctl start tomcat
```

Verify:

```bash
sudo systemctl status tomcat
```

---

# Step 8 - Verify Tomcat

Open:

```
http://<SERVER-IP>:8080
```

Tomcat default page should appear.

---

# Step 9 - Create Maven Web Application

```bash
mkdir ~/hello-webapp

cd ~/hello-webapp

mkdir -p src/main/webapp/WEB-INF
```

---

# Step 10 - Create pom.xml

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>com.yashwanth</groupId>
    <artifactId>hello-webapp</artifactId>
    <version>1.0</version>

    <packaging>war</packaging>

    <name>Hello Web Application</name>

    <build>

        <finalName>hello-webapp</finalName>

        <plugins>

            <plugin>

                <groupId>org.apache.maven.plugins</groupId>

                <artifactId>maven-war-plugin</artifactId>

                <version>3.4.0</version>

            </plugin>

        </plugins>

    </build>

</project>
```

---

# Step 11 - Create index.jsp

```html
<html>

<head>

<title>Hello WebApp</title>

</head>

<body>

<h1>Hello from Version 1</h1>

<h2>Tomcat Deployment using Ansible</h2>

<p>This is Version 1 of the application.</p>

</body>

</html>
```

---

# Step 12 - Create web.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>

<web-app xmlns="https://jakarta.ee/xml/ns/jakartaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee
         https://jakarta.ee/xml/ns/jakartaee/web-app_6_0.xsd"
         version="6.0">

    <display-name>Hello Web Application</display-name>

    <welcome-file-list>
        <welcome-file>index.jsp</welcome-file>
    </welcome-file-list>

</web-app>
```

---

# Step 13 - Build WAR

```bash
cd ~/hello-webapp

mvn clean package
```

Expected:

```
BUILD SUCCESS
```

WAR generated:

```
target/hello-webapp.war
```

---

# Step 14 - Deploy WAR

```bash
sudo cp target/hello-webapp.war /opt/tomcat/webapps/
```

Restart Tomcat:

```bash
sudo systemctl restart tomcat
```

Verify deployment:

```bash
ls -l /opt/tomcat/webapps
```

Expected:

```
hello-webapp/
hello-webapp.war
```

---

# Step 15 - Verify Application

Open:

```
http://<SERVER-IP>:8080/hello-webapp
```

Expected Output:

```
Hello from Version 1

Tomcat Deployment using Ansible

This is Version 1 of the application.
```

---

# Directory Structure

```
hello-webapp
│
├── pom.xml
│
└── src
    └── main
        └── webapp
            ├── index.jsp
            └── WEB-INF
                └── web.xml
```

---

# Next Phase

The application (Version 1) is now deployed manually.

The next step is to use **Ansible** to automate the deployment of **Version 2** from the **Ansible Controller** by:

1. Stopping Tomcat
2. Backing up the existing WAR
3. Deploying the new WAR
4. Starting Tomcat
5. Verifying the application health
