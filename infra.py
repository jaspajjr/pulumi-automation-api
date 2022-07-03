from pulumi_aws import ec2

group = ec2.SecurityGroup('web-secgrp', ingress=[
    {
        "protocol": "tcp",
        "from_port": 80,
        "to_port": 80, "cidr_blocks": ["0.0.0.0/0"]
    },
    ])

def create_instance(instance_name: str):
    server = ec2.Instance(
        'web-server-www;',
        instance_type="t2.micro",
        security_groups=[group.name],  # reference the group object above
        tags={'Name': 'webserver'},     # name tag
        ami="ami-c55673a0")             # AMI for us-east-2 (Ohio)

server = ec2.Instance(
    'web-server-www;',
    instance_type="t2.micro",
    security_groups=[group.name],  # reference the group object above
    tags={'Name': 'webserver'},     # name tag
    ami="ami-c55673a0")             # AMI for us-east-2 (Ohio)
