# Create Java WAR File on Ansible Controller (Version 2)

## Objective

Create a new Java Web Application (Version 2) on the **Ansible Controller**, build it into a WAR file using Maven, and use this WAR for deployment to the target Tomcat server.

---

# Environment

| Component | Details |
|-----------|---------|
| OS | Ubuntu |
| Java | OpenJDK 21 |
| Maven | Apache Maven 3.8.7 |
| Project Location | /opt/ansible/packages/hello-webapp |

---

# Step 1 - Verify Java

```bash
java -version
```

Expected:

```
openjdk version "21.x.x"
```

---

# Step 2 - Verify Maven

```bash
mvn -version
```

Expected:

```
Apache Maven 3.8.7
Java version: 21
```

---

# Step 3 - Create Project Directory

```bash
cd /opt/ansible/packages

mkdir hello-webapp

cd hello-webapp
```

---

# Step 4 - Create Project Structure

```bash
mkdir -p src/main/webapp/WEB-INF
```

Verify:

```bash
tree
```

Expected:

```
.
└── src
    └── main
        └── webapp
            └── WEB-INF
```

---

# Step 5 - Create pom.xml

```bash
vim pom.xml
```

Paste:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>com.yashwanth</groupId>
    <artifactId>hello-webapp</artifactId>
    <version>2.0</version>

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

Save:

```vim
:wq
```

---

# Step 6 - Create index.jsp

```bash
vim src/main/webapp/index.jsp
```

Paste:

```html
<html>
<head>
    <title>Hello WebApp</title>
</head>

<body>

<h1>Hello from Version 2</h1>

<h2>Deployed using Ansible</h2>

<p>This application was deployed from the Ansible Controller.</p>

</body>
</html>
```

Save:

```vim
:wq
```

---

# Step 7 - Create web.xml

```bash
vim src/main/webapp/WEB-INF/web.xml
```

Paste:

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

Save:

```vim
:wq
```

---

# Step 8 - Verify Project Structure

```bash
tree
```

Expected:

```
hello-webapp
├── pom.xml
└── src
    └── main
        └── webapp
            ├── index.jsp
            └── WEB-INF
                └── web.xml
```

---

# Step 9 - Build the WAR File

```bash
cd /opt/ansible/packages/hello-webapp

mvn clean package
```

Expected Output:

```
[INFO] Packaging webapp
[INFO] Building war:
/opt/ansible/packages/hello-webapp/target/hello-webapp.war

[INFO] BUILD SUCCESS
```

---

# Step 10 - Verify Generated WAR

```bash
ls -lh target
```

Expected:

```
target/
├── hello-webapp/
├── hello-webapp.war
└── maven-archiver/
```

---

# Final Directory Structure

```
/opt/ansible/packages/hello-webapp
│
├── pom.xml
├── src
│   └── main
│       └── webapp
│           ├── index.jsp
│           └── WEB-INF
│               └── web.xml
│
└── target
    ├── hello-webapp/
    ├── hello-webapp.war
    └── maven-archiver/
```

---

# Deployment Architecture

```
                Ansible Controller
        /opt/ansible/packages/hello-webapp
                    │
                    │
          mvn clean package
                    │
                    ▼
          target/hello-webapp.war
                    │
                    │
            ansible-playbook
                    │
                    ▼
            Target Tomcat Server
        /opt/tomcat/webapps/
```

---

# Next Phase

The generated WAR file:

```
/opt/ansible/packages/hello-webapp/target/hello-webapp.war
```

will be deployed to the target Tomcat server using an Ansible playbook that performs the following steps:

1. Stop Tomcat
2. Backup existing WAR
3. Remove old deployment
4. Copy new WAR from Ansible Controller
5. Start Tomcat
6. Verify application health
