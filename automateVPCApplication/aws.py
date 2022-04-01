import boto3
from botocore.exceptions import ClientError


class Aws:
    def __init__(self, access_key, secret_access_key):
        self.ap_northeast_2_client = None
        self.us_east_1_client = None
        self.eu_west_2_client = None

        self.dhcp_options_list = ['', '', '']
        self.vpc_list = ['', '', '']
        self.subnet_list = [['', '', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', '']]

        self.access_key = access_key
        self.secret_access_key = secret_access_key

    def createClient(self):
        self.ap_northeast_2_client = boto3.client(
            'ec2',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key,
            region_name='ap-northeast-2'
        )
        self.us_east_1_client = boto3.client(
            'ec2',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key,
            region_name='us-east-1'
        )
        self.eu_west_2_client = boto3.client(
            'ec2',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key,
            region_name='eu-west-2'
        )

    def createDhcpOptions(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_dhcp_options(
                DhcpConfigurations=[
                    {
                        'Key': 'domain-name-servers',
                        'Values': [
                            'AmazonProvidedDNS'
                        ]
                    },
                    {
                        'Key': 'domain-name',
                        'Values': [
                            'ap-northeast-2.compute.internal'
                        ]
                    }
                ],
                TagSpecifications=[
                    {
                        'ResourceType': 'dhcp-options',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-DHCP'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_dhcp_options(
                DhcpConfigurations=[
                    {
                        'Key': 'domain-name-servers',
                        'Values': [
                            'AmazonProvidedDNS'
                        ]
                    },
                    {
                        'Key': 'domain-name',
                        'Values': [
                            'ec2.internal'
                        ]
                    }
                ],
                TagSpecifications=[
                    {
                        'ResourceType': 'dhcp-options',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-DHCP'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_2_response = self.eu_west_2_client.create_dhcp_options(
                DhcpConfigurations=[
                    {
                        'Key': 'domain-name-servers',
                        'Values': [
                            'AmazonProvidedDNS'
                        ]
                    },
                    {
                        'Key': 'domain-name',
                        'Values': [
                            'eu-west-2.compute.internal'
                        ]
                    }
                ],
                TagSpecifications=[
                    {
                        'ResourceType': 'dhcp-options',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-DHCP'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.dhcp_options_list[0] = ap_northeast_2_response['DhcpOptions']['DhcpOptionsId']
            self.dhcp_options_list[1] = us_east_1_response['DhcpOptions']['DhcpOptionsId']
            self.dhcp_options_list[2] = eu_west_2_response['DhcpOptions']['DhcpOptionsId']

        except ClientError as err:
            raise err

    def creatVpc(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_vpc(
                CidrBlock='10.10.0.0/16',
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-VPC'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_vpc(
                CidrBlock='10.20.0.0/16',
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-VPC'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_2_response = self.eu_west_2_client.create_vpc(
                CidrBlock='10.30.0.0/16',
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-VPC'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.vpc_list[0] = ap_northeast_2_response['Vpc']['VpcId']
            self.vpc_list[1] = us_east_1_response['Vpc']['VpcId']
            self.vpc_list[2] = eu_west_2_response['Vpc']['VpcId']

        except ClientError as err:
            raise err

    def associateDhcpOptions(self):
        try:
            self.ap_northeast_2_client.associate_dhcp_options(
                DhcpOptionsId=self.dhcp_options_list[0],
                VpcId=self.vpc_list[0],
            )
            self.us_east_1_client.associate_dhcp_options(
                DhcpOptionsId=self.dhcp_options_list[1],
                VpcId=self.vpc_list[1],
            )
            self.eu_west_2_client.associate_dhcp_options(
                DhcpOptionsId=self.dhcp_options_list[2],
                VpcId=self.vpc_list[2],
            )

        except ClientError as err:
            raise err

    def createSubnetPublicA(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_subnet(
                AvailabilityZone='ap-northeast-2a',
                CidrBlock='10.10.1.0/24',
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PublicSubnetA'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_subnet(
                # TODO: Change to us_east_1
                AvailabilityZone='ap-northeast-2a',
                CidrBlock='10.20.1.0/24',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PublicSubnetA'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_2_client.create_subnet(
                # TODO: Change to eu_west_1
                AvailabilityZone='ap-northeast-2a',
                CidrBlock='10.30.1.0/24',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PublicSubnetA'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.subnet_list[0][0] = ap_northeast_2_response['Subnet']['SubnetId']
            self.subnet_list[1][0] = us_east_1_response['Subnet']['SubnetId']
            self.subnet_list[2][0] = eu_west_1_response['Subnet']['SubnetId']

        except ClientError as err:
            raise err

    def createSubnetPublicB(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_subnet(
                AvailabilityZone='ap-northeast-2b',
                CidrBlock='10.10.2.0/24',
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PublicSubnetB'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_subnet(
                # TODO: Change to us_east_1
                AvailabilityZone='ap-northeast-2b',
                CidrBlock='10.20.2.0/24',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PublicSubnetB'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_2_client.create_subnet(
                # TODO: Change to us_east_1
                AvailabilityZone='ap-northeast-2a',
                CidrBlock='10.30.1.0/24',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PublicSubnetA'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.subnet_list[0][0] = ap_northeast_2_response['Subnet']['SubnetId']
            self.subnet_list[1][0] = us_east_1_response['Subnet']['SubnetId']
            self.subnet_list[2][0] = eu_west_1_response['Subnet']['SubnetId']

        except ClientError as err:
            raise err
