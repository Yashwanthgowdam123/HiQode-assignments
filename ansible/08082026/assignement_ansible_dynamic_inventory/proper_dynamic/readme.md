ubuntu@AnsibleHost:ansible$ ansible-inventory --graph
@all:
  |--@ungrouped:
  |--@aws_ec2:
  |  |--tomcat_prod_2
  |  |--nginx_qa_1
  |  |--nginx_prod_1
  |  |--tomcat_qa_1
  |  |--tomcat_prod_1
  |  |--tomcat_qa_2
  |--@_tomcat:
  |  |--tomcat_prod_2
  |  |--tomcat_qa_1
  |  |--tomcat_prod_1
  |  |--tomcat_qa_2
  |--@_prod:
  |  |--tomcat_prod_2
  |  |--nginx_prod_1
  |  |--tomcat_prod_1
  |--@_tomcat_prod:
  |  |--tomcat_prod_2
  |  |--tomcat_prod_1
  |--@_nginx:
  |  |--nginx_qa_1
  |  |--nginx_prod_1
  |--@_qa:
  |  |--nginx_qa_1
  |  |--tomcat_qa_1
  |  |--tomcat_qa_2
  |--@_nginx_qa:
  |  |--nginx_qa_1
  |--@_nginx_prod:
  |  |--nginx_prod_1
  |--@_tomcat_qa:
  |  |--tomcat_qa_1
  |  |--tomcat_qa_2
ubuntu@AnsibleHost:ansible$ ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml -e "host=_prod" --list-host

playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_prod): Ping all AWS EC2 instances   TAGS: []
    pattern: ['_prod']
    hosts (3):
      tomcat_prod_1
      nginx_prod_1
      tomcat_prod_2
ubuntu@AnsibleHost:ansible$ ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml -e "host=_qa" --list-host

playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_qa): Ping all AWS EC2 instances     TAGS: []
    pattern: ['_qa']
    hosts (3):
      tomcat_qa_1
      nginx_qa_1
      tomcat_qa_2
ubuntu@AnsibleHost:ansible$ ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml -e "host=_tomcat_prod" --list-host

playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_tomcat_prod): Ping all AWS EC2 instances    TAGS: []
    pattern: ['_tomcat_prod']
    hosts (2):
      tomcat_prod_1
      tomcat_prod_2
ubuntu@AnsibleHost:ansible$ ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml -e "host=_tomcat_qa" --list-host

playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_tomcat_qa): Ping all AWS EC2 instances      TAGS: []
    pattern: ['_tomcat_qa']
    hosts (2):
      tomcat_qa_2
      tomcat_qa_1
ubuntu@AnsibleHost:ansible$ ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml -e "host=_prod" --list-host

playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_prod): Ping all AWS EC2 instances   TAGS: []
    pattern: ['_prod']
    hosts (3):
      nginx_prod_1
      tomcat_prod_2
      tomcat_prod_1
ubuntu@AnsibleHost:ansible$ ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml -e "host=_qa" --list-host

playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_qa): Ping all AWS EC2 instances     TAGS: []
    pattern: ['_qa']
    hosts (3):
      tomcat_qa_2
      tomcat_qa_1
      nginx_qa_1
ubuntu@AnsibleHost:ansible$ ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml -e "host=_nginx" --list-host

playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_nginx): Ping all AWS EC2 instances  TAGS: []
    pattern: ['_nginx']
    hosts (2):
      nginx_qa_1
      nginx_prod_1
ubuntu@AnsibleHost:ansible$ ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml -e "host=_nginx_qa" --list-host

playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_nginx_qa): Ping all AWS EC2 instances       TAGS: []
    pattern: ['_nginx_qa']
    hosts (1):
      nginx_qa_1
ubuntu@AnsibleHost:ansible$

