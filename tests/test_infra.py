import pulumi
import unittest


class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + '_id', args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}


pulumi.runtime.set_mocks(
    MyMocks(),
    preview=False,
)


pulumi.runtime.set_mocks(MyMocks())

import infra  # noqa: E402


class TestingWithMocks(unittest.TestCase):
    # check 1: Instances have a Name tag.
    @pulumi.runtime.test
    def test_server_tags(self):
        def check_tags(args):
            urn, tags = args
            self.assertIsNotNone(tags, f'server {urn} must have tags')
            self.assertIn('Name', tags, 'server {urn} must have a name tag')

        return pulumi.Output.all(infra.server.urn, infra.server.tags) \
            .apply(check_tags)

    # check 2: Instances must not use an inline userData script.
    @pulumi.runtime.test
    def test_server_userdata(self):
        def check_user_data(args):
            urn, user_data = args
            self.assertFalse(
                user_data, f'illegal use of user_data on server {urn}')  # noqa

        return pulumi.Output.all(infra.server.urn, infra.server.user_data) \
            .apply(check_user_data)

    # check 3: Test if port 22 for ssh is exposed.
    @pulumi.runtime.test
    def test_security_group_rules(self):
        def check_security_group_rules(args):
            urn, ingress = args
            ssh_open = any(
                [rule['from_port'] == 22 and
                    any(
                        [block == "0.0.0.0/0" for block in rule['cidr_blocks']]
                        )
                    for rule in ingress])
            self.assertFalse(
                ssh_open,
                f'security group {urn} exposes port 22 to the Internet (CIDR 0.0.0.0/0)')  # noqa: E501

        return pulumi.Output.all(infra.group.urn, infra.group.ingress) \
            .apply(check_security_group_rules)
