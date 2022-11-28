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

    def getDistanceBetween(self, address1, address2):
        # print('in DistanceBetween')

        d = self.distanceData[self.addressData.index(address1)][self.addressData.index(address2)]
        if d == '':
            d = self.distanceData[self.addressData.index(address2)][self.addressData.index(address1)]

        return float(d)

    def getMinDistance(self, startingPoint, packages, exclude=None, buddyPackages = 'no'):
        distance = 50
        pack = Package()
        start = startingPoint
        if buddyPackages != 'yes':
            for package in packages:
                for p in package:
                    if p[1].getPackageAddress() != start and exclude is None:
                        if float(self.getDistanceBetween(start, p[1].getPackageAddress())) < float(distance):
                            pack = p[1]
                            distance = self.getDistanceBetween(startingPoint, p[1].getPackageAddress())
                            start = p[1].getPackageAddress()
                    elif exclude is not None and p[1] not in exclude and p[1].getPackageAddress() != start:
                        if float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())) < float(distance):
                            pack = p[1]
                            distance = self.getDistanceBetween(start, p[1].getPackageAddress())
                            start = p[1].getPackageAddress()
        else:
            for package in packages:
                if package.getPackageAddress() != start:
                    if float(self.getDistanceBetween(start, package.getPackageAddress())) < float(distance):
                        pack = package
                        distance = self.getDistanceBetween(start, package.getPackageAddress())
                        start = package.getPackageAddress()


        return pack

    def loadTruck(self, startingPoint, hashMap):
        print('hashMap:', hashMap.getTable())
        if hashMap.getLength() > 12:
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

            #if len(buddyPackages) > 0:
            #    for p in buddyPackages:
            #        self.truck1Packages.append(p)
            #        hashMap.remove(p.getPackageID())



            start = startingPoint
            while len(self.truck2Packages) < 16 and hashMap.isEmpty() is not True:
                package = self.getMinDistance(start, hashMap.getTable())
                self.truck2Packages.append(package)
                self.truck2Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
                hashMap.remove(package.getPackageID())
                start = self.truck2Packages[-1].getPackageAddress()

            while len(self.truck1Packages) < 16 and hashMap.isEmpty() is not True:
                exclude = []
                package = self.getMinDistance(start, hashMap.getTable())
                #if package.getPackageNote() == 'Can only be on truck 2':
                #    while package.getPackageNote() == 'Can only be on truck 2' and hashMap.isEmpty() is not True:
                #        exclude.append(package)
                #        package = self.getMinDistance(start, hashMap.getTable(), exclude)
                #        print('hashMap:', hashMap.getTable())
                #    if package.getPackageID() != 0:
                #        self.truck1Packages.append(package)
                #        print('package:', package.getPackageID())
                #        self.truck1Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
                #        hashMap.remove(package.getPackageID())
                if package.getPackageNote()[:22] == 'Must be delivered with' and (16 - len(self.truck1Packages)) >= len(buddyPackages):
                    self.truck1Packages.append(package)
                    buddyPackages.remove(package)
                    hashMap.remove(package.getPackageID())
                    while len(buddyPackages) > 0:
                        package = self.getMinDistance(start, buddyPackages, package, 'yes')
                        self.truck1Packages.append(package)
                        self.truck1Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
                        buddyPackages.remove(package)
                        hashMap.remove(package.getPackageID())
                        start = self.truck1Packages[-1].getPackageAddress()
                # elif package.getPackageNote() == 'Delayed on flight---will not arrive to depot until 9:05 am':
                #    #TODO: create if statement using timedelta objects to see if package can be loaded
                #    package = self.getMinDistance(start, hashMap.getTable(), package)
                #    self.truck1Packages.append(package)
                #    self.truck1Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
                elif package.getPackageNote() != 'Can only be on truck 2':
                    self.truck1Packages.append(package)
                    self.truck1Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
                    hashMap.remove(package.getPackageID())
                elif package.getPackageNote() == 'Can only be on truck 2':
                    break

                start = self.truck1Packages[-1].getPackageAddress()
        else:
            start = startingPoint
            while len(self.truck2Packages) < 6 and hashMap.isEmpty() is not True:
                package = self.getMinDistance(start, hashMap.getTable())
                self.truck2Packages.append(package)
                self.truck2Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
                hashMap.remove(package.getPackageID())
                start = self.truck2Packages[-1].getPackageAddress()

            while len(self.truck1Packages) < 6 and hashMap.isEmpty() is not True:
                package = self.getMinDistance(start, hashMap.getTable())
                self.truck1Packages.append(package)
                self.truck1Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
                hashMap.remove(package.getPackageID())
                start = self.truck1Packages[-1].getPackageAddress()

    def deliverPackages(self, startingPoint):
        start = startingPoint
        i = 0
        for package in self.truck1Packages:
            d = self.getDistanceBetween(start, package.getPackageAddress())
            self.traveledT1 += d
            start = package.getPackageAddress()
        self.traveledT1 += self.getDistanceBetween(start, startingPoint)
        self.truck1Packages.clear()
        start = startingPoint
        for package in self.truck2Packages:
            d = self.getDistanceBetween(start, package.getPackageAddress())
            self.traveledT2 += d
            start = package.getPackageAddress()
        self.traveledT2 += self.getDistanceBetween(start, startingPoint)
        self.truck2Packages.clear()

    def getTruck1(self, startingPoint):
        start = startingPoint
        #for package in self.truck1Packages:
        #    print('Distance:', self.getDistanceBetween(package.getPackageAddress(), start))
        #    start = package.getPackageAddress()
        #print('Distance:', self.getDistanceBetween(start, startingPoint))
        print('Length:', len(self.truck1Packages))
        for package in self.truck1Packages:
           print('Package ID:', package.getPackageID())

    def getTruck2(self, startingPoint):
        start = startingPoint
        #for package in self.truck2Packages:
        #    print('Distance:', self.getDistanceBetween(package.getPackageAddress(), start))
        #    start = package.getPackageAddress()
        #print('Distance:', self.getDistanceBetween(start, startingPoint))
        print('Length:', len(self.truck2Packages))
        for package in self.truck2Packages:
           print('Package ID:', package.getPackageID())

    def getT1Distance(self):
        return self.traveledT1

    def getT2Distance(self):
        return self.traveledT2

    def getTotalDistance(self):
        return self.traveledT1 + self.traveledT2

    def getTruck1Distance(self):
        return self.truck1Distances

    def getTruck2Distance(self):
        return self.truck2Distances
