from botocore.exceptions import ClientError

from automateVPCApplication.aws import Aws

PROCESS = 60


class Create:
    def __init__(self, access_key, secret_access_key, nat_option, alert_label, progress_bar, progress_bar_val, scrolled_text):
        self.nat_option = nat_option
        self.alert_label = alert_label
        self.progress_bar = progress_bar
        self.progress_bar_val = progress_bar_val
        self.scrolled_text = scrolled_text
        self.aws = Aws(access_key=access_key, secret_access_key=secret_access_key)

    def start(self):
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.delete('1.0', 'end')
        self.scrolled_text.configure(state='disabled')
        self.createClient(1)
        self.createDhcpOptions(2)
        self.createVpcs(3)
        self.associateDhcpOptions(4)
        self.createSubnets(5)
        self.createIGW(6)
        self.attachIGW(7)
        self.createRouteTables(8)
        self.associateSubnetsToRouteTables(9)
        self.createRouteFromIGW(10)
        self.createNetworkAcl(11)
        self.createNetworkAclEntry(12)
        self.replaceNetworkAclAssociationSubnets(13)

        if self.nat_option:
            self.allocateAddressEips(14)
            self.createNatGateways(15)
        else:
            pass

        self.createSecurityGroups(16)

    def createLog(self, text, level):
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert('end', text + '\n', level)
        self.scrolled_text.configure(state='disabled')
        self.scrolled_text.yview('end')

    def updateProgressBar(self, progress):
        self.progress_bar_val.set(100.0 / PROCESS * progress)
        self.progress_bar.update()

    def errorHandler(self, err, err_code):
        self.createLog(err.__str__(), 'ERROR')
        self.alert_label.config(text='Failed.', fg='#ff0000')

        if err_code == 0:
            pass    # createClient and createDhcpOptions Error
        elif err_code == 1:
            self.aws.deleteDhcpOptions()    # createVpcs Error
        else:
            self.aws.deleteAll()    # All Errors

        self.progress_bar_val.set(100.0)
        self.progress_bar.update()

        raise err

    def createClient(self, progress):
        try:
            self.createLog('Trying to connect AWS EC2...', 'INFO')
            self.aws.createClient()
            self.updateProgressBar(progress)

        except ClientError:
            self.errorHandler('AuthFailure : Please check your access key and secret access key.', 0)

            raise ClientError

        except Exception as err:
            self.errorHandler(err, 0)

    def createDhcpOptions(self, progress):
        try:
            self.createLog('Create DHCP Options sets', 'INFO')
            self.aws.createDhcpOptions()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 0)

    def createVpcs(self, progress):
        try:
            self.createLog('Create VPCs', 'INFO')
            self.aws.createVpc()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 1)

    def associateDhcpOptions(self, progress):
        try:
            self.createLog('Associate DHCP Options set to VPC', 'INFO')
            self.aws.associateDhcpOptions()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def createSubnets(self, progress):
        try:
            self.createLog('Create Public Subnet A', 'INFO')
            self.aws.createSubnetPublicA()
            self.createLog('Create Public Subnet B', 'INFO')
            self.aws.createSubnetPublicB()
            self.createLog('Create Private Subnet A', 'INFO')
            self.aws.createSubnetPrivateA()
            self.createLog('Create Private Subnet B', 'INFO')
            self.aws.createSubnetPrivateB()
            self.createLog('Create Database Subnet A', 'INFO')
            self.aws.createSubnetDatabaseA()
            self.createLog('Create Database Subnet B', 'INFO')
            self.aws.createSubnetDatabaseB()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def createIGW(self, progress):
        try:
            self.createLog('Create Internet Gateways', 'INFO')
            self.aws.createInternetGateway()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def attachIGW(self, progress):
        try:
            self.createLog('Attach Internet Gateway to VPC', 'INFO')
            self.aws.attachInternetGateway()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def createRouteTables(self, progress):
        try:
            self.createLog('Create Public Route Table', 'INFO')
            self.aws.createRouteTablePublic()
            self.createLog('Create Private Route Table A', 'INFO')
            self.aws.createRouteTablePrivateA()
            self.createLog('Create Private Route Table B', 'INFO')
            self.aws.createRouteTablePrivateB()
            self.createLog('Create Database Route Table', 'INFO')
            self.aws.createRouteTableDatabase()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def associateSubnetsToRouteTables(self, progress):
        try:
            self.createLog('Associate Public Subnet A to Public Route Table', 'INFO')
            self.aws.associateRouteTablePublicSubnetAPublicRoute()
            self.createLog('Associate Public Subnet B to Public Route Table', 'INFO')
            self.aws.associateRouteTablePublicSubnetBPublicRoute()
            self.createLog('Associate Private Subnet A to Private Route Table A', 'INFO')
            self.aws.associateRouteTablePrivateSubnetAPrivateRouteA()
            self.createLog('Associate Private Subnet B to Private Route Table B', 'INFO')
            self.aws.associateRouteTablePrivateSubnetBPrivateRouteB()
            self.createLog('Associate Database Subnet A to Database Route Table', 'INFO')
            self.aws.associateRouteTableDatabaseSubnetADatabaseRoute()
            self.createLog('Associate Database Subnet B to Database Route Table', 'INFO')
            self.aws.associateRouteTableDatabaseSubnetBDatabaseRoute()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def createRouteFromIGW(self, progress):
        try:
            self.createLog('Create Route From IGW', 'INFO')
            self.aws.createRouteIGW()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def createNetworkAcl(self, progress):
        try:
            self.createLog('Create Network ACLs')
            self.aws.createNetworkAcl()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def createNetworkAclEntry(self, progress):
        try:
            self.createLog('Create Network ACLs\'s Inbound 22 Rule')
            self.aws.createNetworkAclEntryInboundAllow22()
            self.createLog('Create Network ACLs\'s Inbound 80 Rule')
            self.aws.createNetworkAclEntryInboundAllow80()
            self.createLog('Create Network ACLs\'s Inbound 443 Rule')
            self.aws.createNetworkAclEntryInboundAllow443()
            self.createLog('Create Network ACLs\'s Inbound 5234 Rule')
            self.aws.createNetworkAclEntryInboundAllow5234()
            self.createLog('Create Network ACLs\'s Inbound 20222 Rule')
            self.aws.createNetworkAclEntryInboundAllow20222()
            self.createLog('Create Network ACLs\'s Inbound 1024 to 65535 Rule')
            self.aws.createNetworkAclEntryInboundAllow1024To65535()
            self.createLog('Create Network ACLs\'s Outbound All Traffic Rule')
            self.aws.createNetworkAclEntryOutboundAllowAllTraffic()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def replaceNetworkAclAssociationSubnets(self, progress):
        try:
            self.createLog('Replace Network ACL Association Subnets')
            self.aws.replaceNetworkAclAssociationSubnets()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def allocateAddressEips(self, progress):
        try:
            self.createLog('Allocate Elastic IPs')
            self.aws.allocateAddressEipA()
            self.aws.allocateAddressEipB()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def createNatGateways(self, progress):
        try:
            self.createLog('Create NAT Gateways')
            self.aws.createNatGatewayA()
            self.aws.createNatGatewayB()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

    def createSecurityGroups(self, progress):
        try:
            self.createLog('Create Bastion EC2 Server Security Groups')
            self.aws.createSecurityGroupBastion()
            self.createLog('Create ELB Security Groups')
            self.aws.createSecurityGroupELB()
            self.createLog('Create WAS EC2 Server Security Groups')
            self.aws.createSecurityGroupEC2()
            self.createLog('Create RDS Database Server Security Groups')
            self.aws.createSecurityGroupRDS()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err, 2)

