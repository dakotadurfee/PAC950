from hashTable import chainingHash


class Truck:
    def __init__(self, distanceData, addressData):
        self.truck1Packages = []
        self.truck2Packages = []
        self.distanceData = distanceData
        self.addressData = addressData
        self.totalDistance = 0

    def getDistanceBetween(self, address1, address2):
        #print('in DistanceBetween')
        d = self.distanceData[self.addressData.index(address1)][self.addressData.index(address2)]
        if d == '':
            d = self.distanceData[self.addressData.index(address2)][self.addressData.index(address1)]

        return float(d)

    def getMinDistance(self, startingPoint, packages, exclude=None):
        print('In minDistance')
        distance = 50
        i = 0
        for package in packages:
            for p in package:
                if p[1].getPackageAddress() != startingPoint or exclude is None:
                    if float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())) < float(distance):
                        print('Distance:', float(distance))
                        print('Returned distance:', float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())))
                        pack = p[1]
                        distance = self.getDistanceBetween(startingPoint, p[1].getPackageAddress())
                        i += 1
        print('i:', i)

        self.totalDistance += self.getDistanceBetween(startingPoint, p[1].getPackageAddress())
        return pack

    def loadTruck(self, startingPoint, hashMap):
        start = startingPoint
        i = 0
        while len(self.truck1Packages) < 16 or i < 10:
            package = self.getMinDistance(start, hashMap.getTable())
            if package.getPackageNote() != 'Can only be on truck 2':
                self.truck1Packages.append(package)
                print('In loadTruck, Distance:', self.getDistanceBetween(startingPoint, package.getPackageAddress()))
                hashMap.remove(package.getPackageID())
            else:
                package = self.getMinDistance(start, hashMap.getTable(), 0)
                self.truck1Packages.append(package)
                hashMap.remove(package.getPackageID())

            start = self.truck1Packages[-1].getPackageAddress()
            i += 1

        start = startingPoint
        while len(self.truck2Packages) < 16:
            package = self.getMinDistance(start, hashMap.getTable())
            self.truck2Packages.append(package)
            hashMap.remove(package.getPackageID())
            start = self.truck2Packages[-1].getPackageAddress()

    def getTruck1(self):
        print('Length:', len(self.truck1Packages))
        for package in self.truck1Packages:
            print('Package ID:', package.getPackageID())

    def getTruck2(self):
        print('Length:', len(self.truck2Packages))
        for package in self.truck2Packages:
            print('Package ID:', package.getPackageID())

    def getTotalDistance(self):
        return self.totalDistance
