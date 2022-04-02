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
        self.eu_west_1_client = boto3.client(
            'ec2',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key,
            region_name='eu-west-1'
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
                RouteTableId=self.route_table_list[0][1][0]
            )
            self.eu_west_1_client.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                GatewayId=self.internet_gateway_list[2],
                RouteTableId=self.route_table_list[0][2][0]
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
                NatGatewayIds=[
                    self.nat_gateway_id_list[0][0],  # NAT A
                    self.nat_gateway_id_list[0][1],  # NAT B
                ]
            )
            us_east_1_response = self.us_east_1_client.describe_nat_gateways(
                NatGatewayIds=[
                    self.nat_gateway_id_list[1][0],  # NAT A
                    self.nat_gateway_id_list[1][1],  # NAT B
                ]
            )
            eu_west_1_response = self.eu_west_1_client.describe_nat_gateways(
                NatGatewayIds=[
                    self.nat_gateway_id_list[2][0],  # NAT A
                    self.nat_gateway_id_list[2][1],  # NAT B
                ]
            )

            # TODO: Get NAT Gateways' States

        except ClientError as err:
            raise err
