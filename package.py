from hashTable import chainingHash
# Stores the information of a package
class Package:
    def __init__(self, packageID=0, deliveryAddress=None, deliveryDeadline=None, deliveryCity=None, deliveryZip=None,
                 packageWeight=0,
                 specialNote=None):
        self.packageID = packageID
        self.deliveryAddress = deliveryAddress
        self.deliveryDeadline = deliveryDeadline
        self.deliveryCity = deliveryCity
        self.deliveryZip = deliveryZip
        self.packageWeight = packageWeight
        self.specialNote = specialNote
        self.deliveryStatus = False
        self.packageState = 'UT'
        self.deliveryStatus = 'at the hub'

    def getPackageID(self):
        return self.packageID

    def getPackageAddress(self):
        return self.deliveryAddress

    def setPackageAddress(self, address):
        self.deliveryAddress = address

    def getPackageNote(self):
        return self.specialNote

    def setDeliveryStatus(self, status):
        self.deliveryStatus = status

    def getDeliveryStatus(self):
        return self.deliveryStatus

    def getDeliveryDeadline(self):
        return self.deliveryDeadline
