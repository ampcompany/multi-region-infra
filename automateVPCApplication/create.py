from botocore.exceptions import ClientError

from automateVPCApplication.aws import Aws

PROCESS = 60


class Create:
    def __init__(self, access_key, secret_access_key, alert_label, progress_bar, progress_bar_val, scrolled_text):
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

    def createLog(self, text, level):
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert('end', text + '\n', level)
        self.scrolled_text.configure(state='disabled')
        self.scrolled_text.yview('end')

    def updateProgressBar(self, progress):
        self.progress_bar_val.set(100.0 / PROCESS * progress)
        self.progress_bar.update()

    def errorHandler(self, err_str):
        self.createLog(err_str, 'ERROR')
        self.alert_label.config(text='Failed.', fg='#ff0000')
        self.progress_bar_val.set(100.0)
        self.progress_bar.update()

    def createClient(self, progress):
        try:
            self.createLog('Trying to connect AWS EC2...', 'INFO')
            self.aws.createClient()
            self.updateProgressBar(progress)

        except ClientError:
            self.errorHandler('AuthFailure : Please check your access key and secret access key.')

            raise ClientError

        except Exception as err:
            self.errorHandler(err.__str__())

            raise err

    def createDhcpOptions(self, progress):
        try:
            self.createLog('Create DHCP Options sets', 'INFO')
            self.aws.createDhcpOptions()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err.__str__())

            raise err

    def createVpcs(self, progress):
        try:
            self.createLog('Create VPCs', 'INFO')
            self.aws.createVpc()
            self.updateProgressBar(progress)

        except Exception as err:
            self.aws.deleteDhcpOptions()
            self.errorHandler(err.__str__())

            raise err

    def associateDhcpOptions(self, progress):
        try:
            self.createLog('Associate DHCP Options set to VPC', 'INFO')
            self.aws.associateDhcpOptions()
            self.updateProgressBar(progress)

        except Exception as err:
            self.aws.deleteAll()
            self.errorHandler(err.__str__())

            raise err

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
            self.aws.deleteAll()
            self.errorHandler(err.__str__())

            raise err

    def createIGW(self, progress):
        try:
            self.createLog('Create Internet Gateways', 'INFO')
            self.aws.createInternetGateway()
            self.updateProgressBar(progress)

        except Exception as err:
            self.aws.deleteAll()
            self.errorHandler(err.__str__())

    def attachIGW(self, progress):
        try:
            self.createLog('Attach Internet Gateway to VPC', 'INFO')
            self.aws.attachInternetGateway()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err.__str__())

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
            self.errorHandler(err.__str__())

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
            self.errorHandler(err.__str__())

    def createRouteFromIGW(self, progress):
        try:
            self.createLog('Create Route From IGW', 'INFO')
            self.aws.createRouteIGW()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err.__str__())

    def createNetworkAcl(self, progress):
        try:
            self.createLog('Create Network ACLs')
            self.aws.createNetworkAcl()
            self.updateProgressBar(progress)

        except Exception as err:
            self.errorHandler(err.__str__())
