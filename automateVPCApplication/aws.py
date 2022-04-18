import boto3
from botocore.exceptions import ClientError


class Aws:
    def __init__(self, access_key, secret_access_key):
        self.ap_northeast_2_client = None
        self.us_east_1_client = None
        self.eu_west_1_client = None

        self.dhcp_options_list = ['', '', '']
        self.vpc_list = ['', '', '']
        self.subnet_list = [
            [['', ''], ['', ''], ['', '']],  # ap-northeast-2
            [['', ''], ['', ''], ['', '']],  # us-east-1
            [['', ''], ['', ''], ['', '']],  # eu-west-1
        ]
        self.internet_gateway_list = ['', '', '']
        self.route_table_list = [
            [[''], ['', ''], ['']],  # ap-northeast-2
            [[''], ['', ''], ['']],  # us-east-1
            [[''], ['', ''], ['']],  # eu-west-1
        ]
        self.network_acl_list = ['', '', '']
        self.network_acl_association_id_list = [[], [], []]
        self.elastic_ip_allocation_id_list = [
            ['', ''],  # ap-northeast-2
            ['', ''],  # us-east-1
            ['', ''],  # eu-west-1
        ]
        self.nat_gateway_id_list = [
            ['', ''],  # ap-northeast-2
            ['', ''],  # us-east-1
            ['', ''],  # eu-west-1
        ]
        self.security_group_bastion_id_list = ['', '', '']
        self.security_group_elb_id_list = ['', '', '']
        self.security_group_ec2_id_list = ['', '', '']
        self.security_group_rds_id_list = ['', '', '']

        self.access_key = access_key
        self.secret_access_key = secret_access_key

    def createClient(self):
        try:
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
            self.eu_west_1_client = boto3.client(
                'ec2',
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_access_key,
                region_name='eu-west-1'
            )

            ap_northeast_2_response = self.ap_northeast_2_client.describe_vpcs()
            us_east_1_response = self.us_east_1_client.describe_vpcs()
            eu_west_1_response = self.eu_west_1_client.describe_vpcs()

        except ClientError as err:
            raise err

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
            eu_west_1_response = self.eu_west_1_client.create_dhcp_options(
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
                            'eu-west-1.compute.internal'
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
            self.dhcp_options_list[2] = eu_west_1_response['DhcpOptions']['DhcpOptionsId']

        except ClientError as err:
            raise err

    def createVpc(self):
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
            eu_west_1_response = self.eu_west_1_client.create_vpc(
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
            self.vpc_list[2] = eu_west_1_response['Vpc']['VpcId']

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
            self.eu_west_1_client.associate_dhcp_options(
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
                        'ResourceType': 'subnet',
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
                AvailabilityZone='us-east-1a',
                CidrBlock='10.20.1.0/24',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
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
            eu_west_1_response = self.eu_west_1_client.create_subnet(
                AvailabilityZone='eu-west-1a',
                CidrBlock='10.30.1.0/24',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
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

            self.subnet_list[0][0][0] = ap_northeast_2_response['Subnet']['SubnetId']
            self.subnet_list[1][0][0] = us_east_1_response['Subnet']['SubnetId']
            self.subnet_list[2][0][0] = eu_west_1_response['Subnet']['SubnetId']

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
                        'ResourceType': 'subnet',
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
                AvailabilityZone='us-east-1b',
                CidrBlock='10.20.2.0/24',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
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
            eu_west_1_response = self.eu_west_1_client.create_subnet(
                AvailabilityZone='eu-west-1b',
                CidrBlock='10.30.2.0/24',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
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

            self.subnet_list[0][0][1] = ap_northeast_2_response['Subnet']['SubnetId']
            self.subnet_list[1][0][1] = us_east_1_response['Subnet']['SubnetId']
            self.subnet_list[2][0][1] = eu_west_1_response['Subnet']['SubnetId']

        except ClientError as err:
            raise err

    def createSubnetPrivateA(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_subnet(
                AvailabilityZone='ap-northeast-2a',
                CidrBlock='10.10.11.0/24',
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PrivateSubnetA'
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
                AvailabilityZone='us-east-1a',
                CidrBlock='10.20.11.0/24',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PrivateSubnetA'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_subnet(
                AvailabilityZone='eu-west-1a',
                CidrBlock='10.30.11.0/24',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PrivateSubnetA'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.subnet_list[0][1][0] = ap_northeast_2_response['Subnet']['SubnetId']
            self.subnet_list[1][1][0] = us_east_1_response['Subnet']['SubnetId']
            self.subnet_list[2][1][0] = eu_west_1_response['Subnet']['SubnetId']

        except ClientError as err:
            raise err

    def createSubnetPrivateB(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_subnet(
                AvailabilityZone='ap-northeast-2b',
                CidrBlock='10.10.12.0/24',
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PrivateSubnetB'
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
                AvailabilityZone='us-east-1b',
                CidrBlock='10.20.12.0/24',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PrivateSubnetB'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_subnet(
                AvailabilityZone='eu-west-1b',
                CidrBlock='10.30.12.0/24',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-PrivateSubnetB'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.subnet_list[0][1][1] = ap_northeast_2_response['Subnet']['SubnetId']
            self.subnet_list[1][1][1] = us_east_1_response['Subnet']['SubnetId']
            self.subnet_list[2][1][1] = eu_west_1_response['Subnet']['SubnetId']

        except ClientError as err:
            raise err

    def createSubnetDatabaseA(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_subnet(
                AvailabilityZone='ap-northeast-2a',
                CidrBlock='10.10.21.0/24',
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-DatabaseSubnetA'
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
                AvailabilityZone='us-east-1a',
                CidrBlock='10.20.21.0/24',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-DatabaseSubnetA'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_subnet(
                AvailabilityZone='eu-west-1a',
                CidrBlock='10.30.21.0/24',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-DatabaseSubnetA'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.subnet_list[0][2][0] = ap_northeast_2_response['Subnet']['SubnetId']
            self.subnet_list[1][2][0] = us_east_1_response['Subnet']['SubnetId']
            self.subnet_list[2][2][0] = eu_west_1_response['Subnet']['SubnetId']

        except ClientError as err:
            raise err

    def createSubnetDatabaseB(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_subnet(
                AvailabilityZone='ap-northeast-2b',
                CidrBlock='10.10.22.0/24',
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-DatabaseSubnetB'
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
                AvailabilityZone='us-east-1b',
                CidrBlock='10.20.22.0/24',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-DatabaseSubnetB'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_subnet(
                AvailabilityZone='eu-west-1b',
                CidrBlock='10.30.22.0/24',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-DatabaseSubnetB'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.subnet_list[0][2][1] = ap_northeast_2_response['Subnet']['SubnetId']
            self.subnet_list[1][2][1] = us_east_1_response['Subnet']['SubnetId']
            self.subnet_list[2][2][1] = eu_west_1_response['Subnet']['SubnetId']

        except ClientError as err:
            raise err

    def createInternetGateway(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_internet_gateway(
                TagSpecifications=[
                    {
                        'ResourceType': 'internet-gateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-IGW'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_internet_gateway(
                TagSpecifications=[
                    {
                        'ResourceType': 'internet-gateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-IGW'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_internet_gateway(
                TagSpecifications=[
                    {
                        'ResourceType': 'internet-gateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-IGW'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.internet_gateway_list[0] = ap_northeast_2_response['InternetGateway']['InternetGatewayId']
            self.internet_gateway_list[1] = us_east_1_response['InternetGateway']['InternetGatewayId']
            self.internet_gateway_list[2] = eu_west_1_response['InternetGateway']['InternetGatewayId']

        except ClientError as err:
            raise err

    def attachInternetGateway(self):
        try:
            self.ap_northeast_2_client.attach_internet_gateway(
                InternetGatewayId=self.internet_gateway_list[0],
                VpcId=self.vpc_list[0],
            )
            self.us_east_1_client.attach_internet_gateway(
                InternetGatewayId=self.internet_gateway_list[1],
                VpcId=self.vpc_list[1],
            )
            self.eu_west_1_client.attach_internet_gateway(
                InternetGatewayId=self.internet_gateway_list[2],
                VpcId=self.vpc_list[2],
            )

        except ClientError as err:
            raise err

    def createRouteTablePublic(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_route_table(
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Public-Route'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_route_table(
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Public-Route'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_route_table(
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Public-Route'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.route_table_list[0][0][0] = ap_northeast_2_response['RouteTable']['RouteTableId']
            self.route_table_list[1][0][0] = us_east_1_response['RouteTable']['RouteTableId']
            self.route_table_list[2][0][0] = eu_west_1_response['RouteTable']['RouteTableId']

        except ClientError as err:
            raise err

    def createRouteTablePrivateA(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_route_table(
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Private-Route-A'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_route_table(
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Private-Route-A'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_route_table(
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Private-Route-A'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.route_table_list[0][1][0] = ap_northeast_2_response['RouteTable']['RouteTableId']
            self.route_table_list[1][1][0] = us_east_1_response['RouteTable']['RouteTableId']
            self.route_table_list[2][1][0] = eu_west_1_response['RouteTable']['RouteTableId']

        except ClientError as err:
            raise err

    def createRouteTablePrivateB(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_route_table(
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Private-Route-B'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_route_table(
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Private-Route-B'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_route_table(
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Private-Route-B'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.route_table_list[0][1][1] = ap_northeast_2_response['RouteTable']['RouteTableId']
            self.route_table_list[1][1][1] = us_east_1_response['RouteTable']['RouteTableId']
            self.route_table_list[2][1][1] = eu_west_1_response['RouteTable']['RouteTableId']

        except ClientError as err:
            raise err

    def createRouteTableDatabase(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_route_table(
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Database-Route'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_route_table(
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Database-Route'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_route_table(
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Database-Route'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.route_table_list[0][2][0] = ap_northeast_2_response['RouteTable']['RouteTableId']
            self.route_table_list[1][2][0] = us_east_1_response['RouteTable']['RouteTableId']
            self.route_table_list[2][2][0] = eu_west_1_response['RouteTable']['RouteTableId']

        except ClientError as err:
            raise err

    def associateRouteTablePublicSubnetAPublicRoute(self):
        try:
            self.ap_northeast_2_client.associate_route_table(
                RouteTableId=self.route_table_list[0][0][0],
                SubnetId=self.subnet_list[0][0][0],
            )
            self.us_east_1_client.associate_route_table(
                RouteTableId=self.route_table_list[1][0][0],
                SubnetId=self.subnet_list[1][0][0],
            )
            self.eu_west_1_client.associate_route_table(
                RouteTableId=self.route_table_list[2][0][0],
                SubnetId=self.subnet_list[2][0][0],
            )

        except ClientError as err:
            raise err

    def associateRouteTablePublicSubnetBPublicRoute(self):
        try:
            self.ap_northeast_2_client.associate_route_table(
                RouteTableId=self.route_table_list[0][0][0],
                SubnetId=self.subnet_list[0][0][1],
            )
            self.us_east_1_client.associate_route_table(
                RouteTableId=self.route_table_list[1][0][0],
                SubnetId=self.subnet_list[1][0][1],
            )
            self.eu_west_1_client.associate_route_table(
                RouteTableId=self.route_table_list[2][0][0],
                SubnetId=self.subnet_list[2][0][1],
            )

        except ClientError as err:
            raise err

    def associateRouteTablePrivateSubnetAPrivateRouteA(self):
        try:
            self.ap_northeast_2_client.associate_route_table(
                RouteTableId=self.route_table_list[0][1][0],
                SubnetId=self.subnet_list[0][1][0],
            )
            self.us_east_1_client.associate_route_table(
                RouteTableId=self.route_table_list[1][1][0],
                SubnetId=self.subnet_list[1][1][0],
            )
            self.eu_west_1_client.associate_route_table(
                RouteTableId=self.route_table_list[2][1][0],
                SubnetId=self.subnet_list[2][1][0],
            )

        except ClientError as err:
            raise err

    def associateRouteTablePrivateSubnetBPrivateRouteB(self):
        try:
            self.ap_northeast_2_client.associate_route_table(
                RouteTableId=self.route_table_list[0][1][1],
                SubnetId=self.subnet_list[0][1][1],
            )
            self.us_east_1_client.associate_route_table(
                RouteTableId=self.route_table_list[1][1][1],
                SubnetId=self.subnet_list[1][1][1],
            )
            self.eu_west_1_client.associate_route_table(
                RouteTableId=self.route_table_list[2][1][1],
                SubnetId=self.subnet_list[2][1][1],
            )

        except ClientError as err:
            raise err

    def associateRouteTableDatabaseSubnetADatabaseRoute(self):
        try:
            self.ap_northeast_2_client.associate_route_table(
                RouteTableId=self.route_table_list[0][2][0],
                SubnetId=self.subnet_list[0][2][0],
            )
            self.us_east_1_client.associate_route_table(
                RouteTableId=self.route_table_list[1][2][0],
                SubnetId=self.subnet_list[1][2][0],
            )
            self.eu_west_1_client.associate_route_table(
                RouteTableId=self.route_table_list[2][2][0],
                SubnetId=self.subnet_list[2][2][0],
            )

        except ClientError as err:
            raise err

    def associateRouteTableDatabaseSubnetBDatabaseRoute(self):
        try:
            self.ap_northeast_2_client.associate_route_table(
                RouteTableId=self.route_table_list[0][2][1],
                SubnetId=self.subnet_list[0][2][1],
            )
            self.us_east_1_client.associate_route_table(
                RouteTableId=self.route_table_list[1][2][1],
                SubnetId=self.subnet_list[1][2][1],
            )
            self.eu_west_1_client.associate_route_table(
                RouteTableId=self.route_table_list[2][2][1],
                SubnetId=self.subnet_list[2][2][1],
            )

        except ClientError as err:
            raise err

    def createRouteIGW(self):
        try:
            self.ap_northeast_2_client.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                GatewayId=self.internet_gateway_list[0],
                RouteTableId=self.route_table_list[0][0][0]
            )
            self.us_east_1_client.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                GatewayId=self.internet_gateway_list[1],
                RouteTableId=self.route_table_list[1][0][0]
            )
            self.eu_west_1_client.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                GatewayId=self.internet_gateway_list[2],
                RouteTableId=self.route_table_list[2][0][0]
            )

        except ClientError as err:
            raise err

    def createNetworkAcl(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_network_acl(
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'network-acl',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-NACL'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_network_acl(
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'network-acl',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-NACL'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_network_acl(
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'network-acl',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-NACL'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.network_acl_list[0] = ap_northeast_2_response['NetworkAcl']['NetworkAclId']
            self.network_acl_list[1] = us_east_1_response['NetworkAcl']['NetworkAclId']
            self.network_acl_list[2] = eu_west_1_response['NetworkAcl']['NetworkAclId']
            self.network_acl_association_id_list[0] = [
                associationId['NetworkAclAssociationId'] for associationId in
                ap_northeast_2_response['NetworkAcl']['Associations']
            ]
            self.network_acl_association_id_list[1] = [
                associationId['NetworkAclAssociationId'] for associationId in
                us_east_1_response['NetworkAcl']['Associations']
            ]
            self.network_acl_association_id_list[2] = [
                associationId['NetworkAclAssociationId'] for associationId in
                eu_west_1_response['NetworkAcl']['Associations']
            ]

        except ClientError as err:
            raise err

    def createNetworkAclEntryInboundAllow22(self):
        try:
            self.ap_northeast_2_client.create_network_acl_entry(
                CidrBlock='10.0.0.0/8',
                Egress=False,
                NetworkAclId=self.network_acl_list[0],
                PortRange={
                    'From': 22,
                    'To': 22
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=100
            )
            self.us_east_1_client.create_network_acl_entry(
                CidrBlock='10.0.0.0/8',
                Egress=False,
                NetworkAclId=self.network_acl_list[1],
                PortRange={
                    'From': 22,
                    'To': 22
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=100
            )
            self.eu_west_1_client.create_network_acl_entry(
                CidrBlock='10.0.0.0/8',
                Egress=False,
                NetworkAclId=self.network_acl_list[2],
                PortRange={
                    'From': 22,
                    'To': 22
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=100
            )

        except ClientError as err:
            raise err

    def createNetworkAclEntryInboundAllow80(self):
        try:
            self.ap_northeast_2_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[0],
                PortRange={
                    'From': 80,
                    'To': 80
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=200
            )
            self.us_east_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[1],
                PortRange={
                    'From': 80,
                    'To': 80
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=200
            )
            self.eu_west_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[2],
                PortRange={
                    'From': 80,
                    'To': 80
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=200
            )

        except ClientError as err:
            raise err

    def createNetworkAclEntryInboundAllow443(self):
        try:
            self.ap_northeast_2_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[0],
                PortRange={
                    'From': 443,
                    'To': 443
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=300
            )
            self.us_east_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[1],
                PortRange={
                    'From': 443,
                    'To': 443
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=300
            )
            self.eu_west_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[2],
                PortRange={
                    'From': 443,
                    'To': 443
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=300
            )

        except ClientError as err:
            raise err

    def createNetworkAclEntryInboundAllow5234(self):
        try:
            self.ap_northeast_2_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[0],
                PortRange={
                    'From': 443,
                    'To': 443
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=400
            )
            self.us_east_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[1],
                PortRange={
                    'From': 443,
                    'To': 443
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=400
            )
            self.eu_west_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[2],
                PortRange={
                    'From': 443,
                    'To': 443
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=400
            )

        except ClientError as err:
            raise err

    def createNetworkAclEntryInboundAllow20222(self):
        try:
            self.ap_northeast_2_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[0],
                PortRange={
                    'From': 20222,
                    'To': 20222
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=500
            )
            self.us_east_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[1],
                PortRange={
                    'From': 20222,
                    'To': 20222
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=500
            )
            self.eu_west_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[2],
                PortRange={
                    'From': 20222,
                    'To': 20222
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=500
            )

        except ClientError as err:
            raise err

    def createNetworkAclEntryInboundAllow1024To65535(self):
        try:
            self.ap_northeast_2_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[0],
                PortRange={
                    'From': 1024,
                    'To': 65535
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=600
            )
            self.us_east_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[1],
                PortRange={
                    'From': 1024,
                    'To': 65535
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=600
            )
            self.eu_west_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=False,
                NetworkAclId=self.network_acl_list[2],
                PortRange={
                    'From': 1024,
                    'To': 65535
                },
                Protocol='6',  # TCP
                RuleAction='allow',
                RuleNumber=600
            )

        except ClientError as err:
            raise err

    def createNetworkAclEntryOutboundAllowAllTraffic(self):
        try:
            self.ap_northeast_2_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=True,
                NetworkAclId=self.network_acl_list[0],
                Protocol='-1',  # All Traffic
                RuleAction='allow',
                RuleNumber=100
            )
            self.us_east_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=True,
                NetworkAclId=self.network_acl_list[1],
                Protocol='-1',  # All Traffic
                RuleAction='allow',
                RuleNumber=100
            )
            self.eu_west_1_client.create_network_acl_entry(
                CidrBlock='0.0.0.0/0',
                Egress=True,
                NetworkAclId=self.network_acl_list[2],
                Protocol='-1',  # All Traffic
                RuleAction='allow',
                RuleNumber=100
            )

        except ClientError as err:
            raise err

    def replaceNetworkAclAssociationSubnets(self):
        try:
            for i in self.network_acl_association_id_list[0]:
                self.ap_northeast_2_client.replace_network_acl_association(
                    AssociationId=i,
                    NetworkAclId=self.network_acl_list[0]
                )
            for i in self.network_acl_association_id_list[1]:
                self.us_east_1_client.replace_network_acl_association(
                    AssociationId=i,
                    NetworkAclId=self.network_acl_list[1]
                )
            for i in self.network_acl_association_id_list[2]:
                self.eu_west_1_client.replace_network_acl_association(
                    AssociationId=i,
                    NetworkAclId=self.network_acl_list[2]
                )

        except ClientError as err:
            raise err

    def allocateAddressEipA(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.allocate_address(
                TagSpecifications=[
                    {
                        'ResourceType': 'elastic-ip',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EIP-NAT-A'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.allocate_address(
                TagSpecifications=[
                    {
                        'ResourceType': 'elastic-ip',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EIP-NAT-A'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.allocate_address(
                TagSpecifications=[
                    {
                        'ResourceType': 'elastic-ip',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EIP-NAT-A'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.elastic_ip_allocation_id_list[0][0] = ap_northeast_2_response['AllocationId']
            self.elastic_ip_allocation_id_list[1][0] = us_east_1_response['AllocationId']
            self.elastic_ip_allocation_id_list[2][0] = eu_west_1_response['AllocationId']

        except ClientError as err:
            raise err

    def allocateAddressEipB(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.allocate_address(
                TagSpecifications=[
                    {
                        'ResourceType': 'elastic-ip',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EIP-NAT-B'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.allocate_address(
                TagSpecifications=[
                    {
                        'ResourceType': 'elastic-ip',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EIP-NAT-B'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.allocate_address(
                TagSpecifications=[
                    {
                        'ResourceType': 'elastic-ip',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EIP-NAT-B'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.elastic_ip_allocation_id_list[0][1] = ap_northeast_2_response['AllocationId']
            self.elastic_ip_allocation_id_list[1][1] = us_east_1_response['AllocationId']
            self.elastic_ip_allocation_id_list[2][1] = eu_west_1_response['AllocationId']

        except ClientError as err:
            raise err

    def createNatGatewayA(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_nat_gateway(
                AllocationId=self.elastic_ip_allocation_id_list[0][0],
                SubnetId=self.subnet_list[0][0][0],
                TagSpecifications=[
                    {
                        'ResourceType': 'natgateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-NAT-A'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_nat_gateway(
                AllocationId=self.elastic_ip_allocation_id_list[1][0],
                SubnetId=self.subnet_list[0][1][0],
                TagSpecifications=[
                    {
                        'ResourceType': 'natgateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-NAT-A'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_nat_gateway(
                AllocationId=self.elastic_ip_allocation_id_list[2][0],
                SubnetId=self.subnet_list[0][2][0],
                TagSpecifications=[
                    {
                        'ResourceType': 'natgateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-NAT-A'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.nat_gateway_id_list[0][0] = ap_northeast_2_response['NatGateway']['NatGatewayId']
            self.nat_gateway_id_list[1][0] = us_east_1_response['NatGateway']['NatGatewayId']
            self.nat_gateway_id_list[2][0] = eu_west_1_response['NatGateway']['NatGatewayId']

        except ClientError as err:
            raise err

    def createNatGatewayB(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_nat_gateway(
                AllocationId=self.elastic_ip_allocation_id_list[0][1],
                SubnetId=self.subnet_list[0][0][1],
                TagSpecifications=[
                    {
                        'ResourceType': 'natgateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-NAT-B'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_nat_gateway(
                AllocationId=self.elastic_ip_allocation_id_list[1][1],
                SubnetId=self.subnet_list[0][1][1],
                TagSpecifications=[
                    {
                        'ResourceType': 'natgateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-NAT-B'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_nat_gateway(
                AllocationId=self.elastic_ip_allocation_id_list[2][1],
                SubnetId=self.subnet_list[0][2][1],
                TagSpecifications=[
                    {
                        'ResourceType': 'natgateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-NAT-B'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.nat_gateway_id_list[0][1] = ap_northeast_2_response['NatGateway']['NatGatewayId']
            self.nat_gateway_id_list[1][1] = us_east_1_response['NatGateway']['NatGatewayId']
            self.nat_gateway_id_list[2][1] = eu_west_1_response['NatGateway']['NatGatewayId']

        except ClientError as err:
            raise err

    def describeNatGateways(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.describe_nat_gateways(
                NatGatewayIds=self.nat_gateway_id_list[0]
            )
            us_east_1_response = self.us_east_1_client.describe_nat_gateways(
                NatGatewayIds=self.nat_gateway_id_list[1]
            )
            eu_west_1_response = self.eu_west_1_client.describe_nat_gateways(
                NatGatewayIds=self.nat_gateway_id_list[2]
            )

            nat_gateways_states = {
                'ap-northeast-2': [
                    {
                        'State': nat_gateway['State'],
                        'FailureMessage': nat_gateway['FailureMessage'],
                        'AvailabilityZone':
                            next((tag['Value'] for tag in nat_gateway['Tags'] if tag['Key'] == 'Name'), False)[-1]
                    } for nat_gateway in ap_northeast_2_response['NatGateways']
                ],
                'us-east-1': [
                    {
                        'State': nat_gateway['State'],
                        'FailureMessage': nat_gateway['FailureMessage'],
                        'AvailabilityZone':
                            next((tag['Value'] for tag in nat_gateway['Tags'] if tag['Key'] == 'Name'), False)[-1]
                    } for nat_gateway in us_east_1_response['NatGateways']
                ],
                'eu-west-1': [
                    {
                        'State': nat_gateway['State'],
                        'FailureMessage': nat_gateway['FailureMessage'],
                        'AvailabilityZone':
                            next((tag['Value'] for tag in nat_gateway['Tags'] if tag['Key'] == 'Name'), False)[-1]
                    } for nat_gateway in eu_west_1_response['NatGateways']
                ]
            }

        except ClientError as err:
            raise err

    def createRouteNatA(self):
        try:
            self.ap_northeast_2_client.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                NatGatewayId=self.nat_gateway_id_list[0][0],
                RouteTableId=self.route_table_list[0][1][0]
            )
            self.us_east_1_client.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                NatGatewayId=self.nat_gateway_id_list[1][0],
                RouteTableId=self.route_table_list[1][1][0]
            )
            self.eu_west_1_client.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                NatGatewayId=self.nat_gateway_id_list[2][0],
                RouteTableId=self.route_table_list[2][1][0]
            )

        except ClientError as err:
            raise err

    def createRouteNatB(self):
        try:
            self.ap_northeast_2_client.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                NatGatewayId=self.nat_gateway_id_list[0][1],
                RouteTableId=self.route_table_list[0][1][1]
            )
            self.us_east_1_client.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                NatGatewayId=self.nat_gateway_id_list[1][1],
                RouteTableId=self.route_table_list[1][1][1]
            )
            self.eu_west_1_client.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                NatGatewayId=self.nat_gateway_id_list[2][1],
                RouteTableId=self.route_table_list[2][1][1]
            )

        except ClientError as err:
            raise err

    def createSecurityGroupBastion(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_security_group(
                Description='Security Group for Bastion EC2 Server.',
                GroupName='MR-Bastion-SG',
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Bastion-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_security_group(
                Description='Security Group for Bastion EC2 Server.',
                GroupName='MR-Bastion-SG',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Bastion-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_security_group(
                Description='Security Group for Bastion EC2 Server.',
                GroupName='MR-Bastion-SG',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Bastion-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.security_group_bastion_id_list[0] = ap_northeast_2_response['GroupId']
            self.security_group_bastion_id_list[1] = us_east_1_response['GroupId']
            self.security_group_bastion_id_list[2] = eu_west_1_response['GroupId']

        except ClientError as err:
            raise err

    def createSecurityGroupELB(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_security_group(
                Description='Security Group for Elastic Load Balancer.',
                GroupName='MR-ELB-SG',
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_security_group(
                Description='Security Group for Elastic Load Balancer.',
                GroupName='MR-ELB-SG',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_security_group(
                Description='Security Group for Elastic Load Balancer.',
                GroupName='MR-ELB-SG',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.security_group_elb_id_list[0] = ap_northeast_2_response['GroupId']
            self.security_group_elb_id_list[1] = us_east_1_response['GroupId']
            self.security_group_elb_id_list[2] = eu_west_1_response['GroupId']

        except ClientError as err:
            raise err

    def createSecurityGroupEC2(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_security_group(
                Description='Security Group for WAS EC2 Server.',
                GroupName='MR-EC2-SG',
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EC2-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_security_group(
                Description='Security Group for WAS EC2 Server.',
                GroupName='MR-EC2-SG',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EC2-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_security_group(
                Description='Security Group for WAS EC2 Server.',
                GroupName='MR-EC2-SG',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EC2-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.security_group_ec2_id_list[0] = ap_northeast_2_response['GroupId']
            self.security_group_ec2_id_list[1] = us_east_1_response['GroupId']
            self.security_group_ec2_id_list[2] = eu_west_1_response['GroupId']

        except ClientError as err:
            raise err

    def createSecurityGroupRDS(self):
        try:
            ap_northeast_2_response = self.ap_northeast_2_client.create_security_group(
                Description='Security Group for Database RDS Server.',
                GroupName='MR-RDS-SG',
                VpcId=self.vpc_list[0],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-RDS-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            us_east_1_response = self.us_east_1_client.create_security_group(
                Description='Security Group for Database RDS Server.',
                GroupName='MR-RDS-SG',
                VpcId=self.vpc_list[1],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-RDS-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            eu_west_1_response = self.eu_west_1_client.create_security_group(
                Description='Security Group for Database RDS Server.',
                GroupName='MR-RDS-SG',
                VpcId=self.vpc_list[2],
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-RDS-SG'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

            self.security_group_rds_id_list[0] = ap_northeast_2_response['GroupId']
            self.security_group_rds_id_list[1] = us_east_1_response['GroupId']
            self.security_group_rds_id_list[2] = eu_west_1_response['GroupId']

        except ClientError as err:
            raise err

    def authorizeSecurityGroupIngressBastionSgFrom20222(self):
        try:
            self.ap_northeast_2_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=20222,
                GroupId=self.security_group_bastion_id_list[0],
                IpProtocol='tcp',
                ToPort=20222,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Bastion-SG-Inbound-Rule-Allow-20222'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.us_east_1_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=20222,
                GroupId=self.security_group_bastion_id_list[1],
                IpProtocol='tcp',
                ToPort=20222,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Bastion-SG-Inbound-Rule-Allow-20222'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.eu_west_1_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=20222,
                GroupId=self.security_group_bastion_id_list[2],
                IpProtocol='tcp',
                ToPort=20222,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Bastion-SG-Inbound-Rule-Allow-20222'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

        except ClientError as err:
            raise err

    def authorizeSecurityGroupEgressBastionSgToAllTraffic(self):
        try:
            self.ap_northeast_2_client.authorize_security_group_egress(
                CidrIp='0.0.0.0/0',
                GroupId=self.security_group_bastion_id_list[0],
                IpProtocol='-1',
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Bastion-SG-Outbound-Rule-Allow-All-Traffic'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.us_east_1_client.authorize_security_group_egress(
                CidrIp='0.0.0.0/0',
                GroupId=self.security_group_bastion_id_list[1],
                IpProtocol='-1',
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Bastion-SG-Outbound-Rule-Allow-All-Traffic'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.eu_west_1_client.authorize_security_group_egress(
                CidrIp='0.0.0.0/0',
                GroupId=self.security_group_bastion_id_list[2],
                IpProtocol='-1',
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-Bastion-SG-Outbound-Rule-Allow-All-Traffic'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

        except ClientError as err:
            raise err

    def authorizeSecurityGroupIngressElbSgFrom80(self):
        try:
            self.ap_northeast_2_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=80,
                GroupId=self.security_group_elb_id_list[0],
                IpProtocol='tcp',
                ToPort=80,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG-Inbound-Rule-Allow-80'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.us_east_1_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=80,
                GroupId=self.security_group_elb_id_list[1],
                IpProtocol='tcp',
                ToPort=80,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG-Inbound-Rule-Allow-80'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.eu_west_1_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=80,
                GroupId=self.security_group_elb_id_list[2],
                IpProtocol='tcp',
                ToPort=80,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG-Inbound-Rule-Allow-80'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

        except ClientError as err:
            raise err

    def authorizeSecurityGroupIngressElbSgFrom443(self):
        try:
            self.ap_northeast_2_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=443,
                GroupId=self.security_group_elb_id_list[0],
                IpProtocol='tcp',
                ToPort=443,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG-Inbound-Rule-Allow-443'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.us_east_1_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=443,
                GroupId=self.security_group_elb_id_list[1],
                IpProtocol='tcp',
                ToPort=443,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG-Inbound-Rule-Allow-443'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.eu_west_1_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=443,
                GroupId=self.security_group_elb_id_list[2],
                IpProtocol='tcp',
                ToPort=443,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG-Inbound-Rule-Allow-443'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

        except ClientError as err:
            raise err

    def authorizeSecurityGroupEgressElbSgToAllTraffic(self):
        try:
            self.ap_northeast_2_client.authorize_security_group_egress(
                CidrIp='0.0.0.0/0',
                GroupId=self.security_group_elb_id_list[0],
                IpProtocol='-1',
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG-Outbound-Rule-Allow-All-Traffic'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.us_east_1_client.authorize_security_group_egress(
                CidrIp='0.0.0.0/0',
                GroupId=self.security_group_elb_id_list[1],
                IpProtocol='-1',
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG-Outbound-Rule-Allow-All-Traffic'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.eu_west_1_client.authorize_security_group_egress(
                CidrIp='0.0.0.0/0',
                GroupId=self.security_group_elb_id_list[2],
                IpProtocol='-1',
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-ELB-SG-Outbound-Rule-Allow-All-Traffic'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

        except ClientError as err:
            raise err

    def authorizeSecurityGroupIngressEc2SgFrom22(self):
        # TODO: Add BastionSG Source Security Group
        try:
            self.ap_northeast_2_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                GroupId=self.security_group_ec2_id_list[0],
                IpProtocol='tcp',

                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EC2-SG-Inbound-Rule-Allow-22'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.us_east_1_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                GroupId=self.security_group_ec2_id_list[1],
                IpProtocol='tcp',

                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EC2-SG-Inbound-Rule-Allow-22'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.eu_west_1_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                GroupId=self.security_group_ec2_id_list[2],
                IpProtocol='tcp',

                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EC2-SG-Inbound-Rule-Allow-22'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

        except ClientError as err:
            raise err

    def authorizeSecurityGroupIngressEc2SgFrom80(self):
        try:
            self.ap_northeast_2_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=80,
                GroupId=self.security_group_ec2_id_list[0],
                IpProtocol='tcp',
                ToPort=80,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EC2-SG-Inbound-Rule-Allow-80'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.us_east_1_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=80,
                GroupId=self.security_group_ec2_id_list[1],
                IpProtocol='tcp',
                ToPort=80,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EC2-SG-Inbound-Rule-Allow-80'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )
            self.eu_west_1_client.authorize_security_group_ingress(
                CidrIp='0.0.0.0/0',
                FromPort=80,
                GroupId=self.security_group_ec2_id_list[2],
                IpProtocol='tcp',
                ToPort=80,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group-rule',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'MR-EC2-SG-Inbound-Rule-Allow-80'
                            },
                            {
                                'Key': 'Project',
                                'Value': 'Multi-Region'
                            }
                        ]
                    }
                ]
            )

        except ClientError as err:
            raise err

    # TODO: Add other security groups

    # def authorizeSecurityGroup

    def deleteDhcpOptions(self):
        self.ap_northeast_2_client.delete_dhcp_options(
            DhcpOptionsId=self.dhcp_options_list[0]
        )
        self.us_east_1_client.delete_dhcp_options(
            DhcpOptionsId=self.dhcp_options_list[1]
        )
        self.eu_west_1_client.delete_dhcp_options(
            DhcpOptionsId=self.dhcp_options_list[2]
        )

    def deleteVpc(self):
        self.ap_northeast_2_client.delete_vpc(
            VpcId=self.vpc_list[0]
        )
        self.us_east_1_client.delete_vpc(
            VpcId=self.vpc_list[1]
        )
        self.eu_west_1_client.delete_vpc(
            VpcId=self.vpc_list[2]
        )

    def deleteAll(self):
        self.deleteVpc()
        self.deleteDhcpOptions()
