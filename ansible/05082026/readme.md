1. write a playbook to install nginx, and change the port from 80 to 8081 and deploy some application into it.

2. Install tomcat using playbook and change the port 8080 to 9090.

3. write a playbook to get the Target instances report below:
Cpu
Ram
Storage
hostname

4. create your own custom inventory file and ansible.cfg file where declare private, key user in inventory. At least you should have:
webserver
    web-01
    web-02

appserver
    app-01
    app-02

dbserver
    db-01
