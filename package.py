from hashTable import chainingHash


class Package:
    def __init__(self, packageID, deliveryAddress, deliveryDeadline, deliveryCity, deliveryZip, packageWeight,
                 specialNote):
        self.packageID = packageID
        self.deliveryAddress = deliveryAddress
        self.deliveryDeadline = deliveryDeadline
        self.deliveryCity = deliveryCity
        self.deliveryZip = deliveryZip
        self.packageWeight = packageWeight
        self.specialNote = specialNote
        self.deliveryStatus = False
        self.packageState = 'UT'

    def getPackageID(self):
        return self.packageID

    def getPackageAddress(self):
        return self.deliveryAddress

    def getPackageNote(self):
        return self.specialNote
