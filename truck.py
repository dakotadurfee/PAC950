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
        self.traveledT1 = 0
        self.traveledT2 = 0
        self.totalDistance = 0

    def getDistanceBetween(self, address1, address2):
        # print('in DistanceBetween')

        d = self.distanceData[self.addressData.index(address1)][self.addressData.index(address2)]
        if d == '':
            d = self.distanceData[self.addressData.index(address2)][self.addressData.index(address1)]

        return float(d)

    def getMinDistance(self, startingPoint, packages, exclude=None):
        distance = 50
        pack = Package()
        start = startingPoint
        for package in packages:
            for p in package:
                if p[1].getPackageAddress() != start and exclude is None:
                    if float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())) < float(distance):
                        pack = p[1]
                        distance = self.getDistanceBetween(startingPoint, p[1].getPackageAddress())
                        start = p[1].getPackageAddress()
                elif float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())) < float(distance) and p[
                    1] != exclude and p[1].getPackageAddress() != start:
                    pack = p[1]
                    distance = self.getDistanceBetween(startingPoint, p[1].getPackageAddress())
                    start = p[1].getPackageAddress()

        self.totalDistance += distance
        # print('totalDistance +=', self.getDistanceBetween(startingPoint, p[1].getPackageAddress()))
        return pack

    def loadTruck(self, startingPoint, hashMap):
        start = startingPoint
        buddyPackages = []
        for row in hashMap.getTable():
            for column in row:
                note = column[1].getPackageNote()
                if note[:22] == 'Must be delivered with':
                    buddyPackages.append(column[1])
                    if hashMap.search(note[23:25]) not in buddyPackages:
                        buddyPackages.append(hashMap.search(note[23:25]))
                    elif hashMap.search(note[26:]) not in buddyPackages:
                        buddyPackages.append(hashMap.search(note[26:]))

        for p in buddyPackages:
            self.truck1Packages.append(p)
            hashMap.remove(p.getPackageID())


        while len(self.truck1Packages) < 16 and hashMap.isEmpty() != True:
            package = self.getMinDistance(start, hashMap.getTable())
            if package.getPackageNote() == 'Can only be on truck 2':
                while package.getPackageNote() == 'Can only be on truck 2':
                    package = self.getMinDistance(start, hashMap.getTable(), package)
                self.truck1Packages.append(package)
                self.truck1Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
                hashMap.remove(package.getPackageID())
            elif package.getPackageNote() == 'Delayed on flight---will not arrive to depot until 9:05 am':
                #TODO: create if statement using timedelta objects to see if package can be loaded
                package = self.getMinDistance(start, hashMap.getTable(), package)
                self.truck1Packages.append(package)
                self.truck1Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
            else:
                package = self.getMinDistance(start, hashMap.getTable(), package)
                self.truck1Packages.append(package)
                self.truck1Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
                hashMap.remove(package.getPackageID())

            start = self.truck1Packages[-1].getPackageAddress()

        start = startingPoint
        while len(self.truck2Packages) < 16:
            package = self.getMinDistance(start, hashMap.getTable())
            self.truck2Packages.append(package)
            self.truck2Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
            hashMap.remove(package.getPackageID())
            start = self.truck2Packages[-1].getPackageAddress()

    def deliveryPackages(self):


    def getTruck1(self):
        print('Length:', len(self.truck1Packages))
        for package in self.truck1Packages:
            print('Package Note:', package.getPackageNote())

    def getTruck2(self):
        print('Length:', len(self.truck2Packages))
        for package in self.truck2Packages:
            print('Package Note:', package.getPackageNote())

    def getTotalDistance(self):
        return self.totalDistance

    def getTruck1Distance(self):
        return self.truck1Distances

    def getTruck2Distance(self):
        return self.truck2Distances
