from hashTable import chainingHash
from package import Package

class Truck:
    def __init__(self, distanceData, addressData):
        self.truck1Packages = []
        self.truck1Distances = []
        self.truck2Packages = []
        self.truck2Distances = []
        self.distanceData = distanceData
        self.addressData = addressData
        self.totalDistance = 0

    def getDistanceBetween(self, address1, address2):
        #print('in DistanceBetween')
        d = self.distanceData[self.addressData.index(address1)][self.addressData.index(address2)]
        if d == '':
            d = self.distanceData[self.addressData.index(address2)][self.addressData.index(address1)]

        return float(d)

    def getMinDistance(self, startingPoint, packages, myHash, exclude=None):
        distance = 50
        pack = None
        for package in packages:
            for p in package:
                if p[1].getPackageAddress() != startingPoint and exclude is None:
                    if float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())) < float(distance):
                        print('Distance:', float(distance))
                        print('Returned distance:', float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())))
                        pack = p[1]
                        distance = self.getDistanceBetween(startingPoint, p[1].getPackageAddress())

        self.totalDistance += distance
        print('Hash Map:', myHash.getTable())
        #print('totalDistance +=', self.getDistanceBetween(startingPoint, p[1].getPackageAddress()))
        return pack

    def loadTruck(self, startingPoint, hashMap):
        start = startingPoint

        while len(self.truck1Packages) < 16:
            package = self.getMinDistance(start, hashMap.getTable(), hashMap)
            #if package.getPackageNote() != 'Can only be on truck 2':
            #    self.truck1Packages.append(package)
            #    self.truck1Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
            #    #print('In loadTruck, Distance:', self.getDistanceBetween(start, package.getPackageAddress()))
            #    hashMap.remove(package.getPackageID())
            if package.getPackageNote() == 'Must be delivered with 13, 15' and len(self.truck1Packages) < 14:
                package = hashMap.search(package.getPackageID())
                self.truck1Distances.append(package)
                self.truck1Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
                hashMap.remove(package.getPackageID())
            else:
                package = self.getMinDistance(start, hashMap.getTable(), package, hashMap)
                print('package:', package.getPackageAddress())
                self.truck1Packages.append(package)
                print('In loadTruck else, Distance:', self.getDistanceBetween(start,package.getPackageAddress()))
                hashMap.remove(package.getPackageID())

            start = self.truck1Packages[-1].getPackageAddress()

        start = startingPoint
        while len(self.truck2Packages) < 16:
            package = self.getMinDistance(start, hashMap.getTable(), hashMap)
            self.truck2Packages.append(package)
            self.truck2Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
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

    def getTruck1Distance(self):
        return self.truck1Distances

    def getTruck2Distance(self):
        return self.truck2Distances
