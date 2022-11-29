from hashTable import chainingHash
from package import Package


class Truck:
    def __init__(self, distanceData, addressData):
        self.truck1Packages = []
        self.truck2Packages = []
        self.distanceData = distanceData
        self.addressData = addressData
        self.traveledT1 = 0
        self.traveledT2 = 0
        self.numLoads = 0
        self.truck1Distances = []
        self.truck2Distances = []
        self.tempDistanceT1 = 0
        self.tempDistanceT2 = 0

    def getDistanceBetween(self, address1, address2, p14 = 'no'):
        # print('in DistanceBetween')
        #print('address 1:', address1)
        #print('address 2:', address2)
        if p14 == 'yes':
            print('address1:', address1)
            print('address2:', address2)

        d = self.distanceData[self.addressData.index(address1)][self.addressData.index(address2)]
        if d == '':
            d = self.distanceData[self.addressData.index(address2)][self.addressData.index(address1)]

        return float(d)

    def getMinDistance(self, startingPoint, packages, exclude=None, buddyPackages = 'no'):
        distance = 50
        pack = Package()
        start = startingPoint

        if buddyPackages == 'no':
            for package in packages:
                for p in package:
                    if p[1].getPackageAddress() != start and exclude is None:
                        #print('package:', p[1].getPackageAddress())

                        if float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())) < float(distance):
                            pack = p[1]
                            distance = self.getDistanceBetween(startingPoint, p[1].getPackageAddress())
                            #start = p[1].getPackageAddress()
                    elif exclude is not None and p[1] not in exclude and p[1].getPackageAddress() != start:
                        if float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())) < float(distance):
                            pack = p[1]
                            distance = self.getDistanceBetween(start, p[1].getPackageAddress())
                            #start = p[1].getPackageAddress()
        else:
            if exclude == None:
                for package in packages:
                    if package.getPackageAddress() != start or len(packages) == 1:
                        if float(self.getDistanceBetween(start, package.getPackageAddress())) < float(distance):
                            pack = package
                            distance = self.getDistanceBetween(start,package.getPackageAddress())
                            start = package.getPackageAddress()
            else:
                for package in packages:
                    if package not in exclude and float(self.getDistanceBetween(start, package.getPackageAddress())) < float(distance):
                        pack = package
                        distance = self.getDistanceBetween(start,package.getPackageAddress())
                        start = package.getPackageAddress()


        return pack

    def loadTruck(self, startingPoint, hashMap):
        start = startingPoint
        buddyPackages = []
        self.numLoads += 1
        for row in hashMap.getTable():
            for column in row:
                note = column[1].getPackageNote()
                if note[:22] == 'Must be delivered with':
                    buddyPackages.append(column[1])
                    if hashMap.search(note[23:25]) not in buddyPackages:
                        buddyPackages.append(hashMap.search(note[23:25]))
                    elif hashMap.search(note[26:]) not in buddyPackages:
                        buddyPackages.append(hashMap.search(note[26:]))

        if self.numLoads <= 1:
            while len(self.truck1Packages) < 16 and hashMap.isEmpty() != True:
                package = self.getMinDistance(start, hashMap.getTable())
                exclude = []
                if package.getPackageNote() == 'Can only be on truck 2':
                    while package.getPackageNote() == 'Can only be on truck 2':
                        exclude.append(package)
                        package = self.getMinDistance(start, hashMap.getTable(), exclude)
                        start = package.getPackageAddress()
                    self.truck1Packages.append(package)
                    hashMap.remove(package.getPackageID())
                elif package.getPackageNote()[:7] == 'Delayed' and self.numLoads <= 1:
                    pack = package
                    exclude.append(pack)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                    self.truck1Packages.append(package)
                    start = package.getPackageAddress()
                    hashMap.remove(package.getPackageID())
                elif package.getPackageNote()[:7] == 'Delayed' and self.numLoads > 1:
                    self.truck1Packages.append(package)
                    start = package.getPackageAddress()
                    hashMap.remove(package.getPackageID())
                elif package.getPackageNote()[:5] == 'Wrong' and self.numLoads <= 1:
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                    self.truck1Packages.append(package)
                    start = package.getPackageAddress()
                    hashMap.remove(package.getPackageID())
                elif package.getPackageNote()[:5] == 'Wrong' and self.numLoads > 1:
                    self.truck1Packages.append(package)
                    start = package.getPackageAddress()
                    hashMap.remove(package.getPackageID())
                elif package in buddyPackages:
                    self.truck1Packages.append(package)
                    buddyPackages.remove(package)
                    hashMap.remove(package.getPackageID())
                    while len(buddyPackages) > 0:
                        package = self.getMinDistance(start, buddyPackages, None, 'yes')
                        self.truck1Packages.append(package)
                        buddyPackages.remove(package)
                        hashMap.remove(package.getPackageID())
                        start = self.truck1Packages[-1].getPackageAddress()
                elif package.getPackageNote() == '':
                    self.truck1Packages.append(package)
                    start = package.getPackageAddress()
                    hashMap.remove(package.getPackageID())

            start = startingPoint
            while len(self.truck2Packages) < 16 and hashMap.isEmpty() != True:
                package = self.getMinDistance(start, hashMap.getTable())
                self.truck2Packages.append(package)
                hashMap.remove(package.getPackageID())
                start = package.getPackageAddress()

        else:
            while len(self.truck2Packages) < 4 and hashMap.isEmpty() != True:
                package = self.getMinDistance(start, hashMap.getTable())
                self.truck2Packages.append(package)
                hashMap.remove(package.getPackageID())
                start = package.getPackageAddress()

            while len(self.truck1Packages) < 4 and hashMap.isEmpty() != True:
                package = self.getMinDistance(start, hashMap.getTable())
                self.truck1Packages.append(package)
                hashMap.remove(package.getPackageID())
                start = package.getPackageAddress()

    def deliverPackages(self, startingPoint):
        start = startingPoint
        i = 0
        for package in self.truck1Packages:
            self.traveledT1 += self.getDistanceBetween(start, package.getPackageAddress())
            self.truck1Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
            start = package.getPackageAddress()

        self.traveledT1 += self.getDistanceBetween(start, startingPoint)
        self.truck1Distances.append(self.getDistanceBetween(start,startingPoint))
        self.truck1Packages.clear()
        start = startingPoint

        for package in self.truck2Packages:
            self.traveledT2 += self.getDistanceBetween(start, package.getPackageAddress())
            self.truck2Distances.append(self.getDistanceBetween(start, package.getPackageAddress()))
            start = package.getPackageAddress()

        self.traveledT2 += self.getDistanceBetween(start, startingPoint)
        self.truck2Distances.append(self.getDistanceBetween(start, startingPoint))
        self.truck2Packages.clear()

    def getTruck1(self, startingPoint):
        start = startingPoint
        #for package in self.truck1Packages:
        #    print('Distance:', self.getDistanceBetween(package.getPackageAddress(), start))
        #    start = package.getPackageAddress()
        #print('Distance:', self.getDistanceBetween(start, startingPoint))
        for package in self.truck1Packages:
           print('Package ID:', package.getPackageID())

    def getTruck2(self, startingPoint):
        start = startingPoint
        #for package in self.truck2Packages:
        #    print('Distance:', self.getDistanceBetween(package.getPackageAddress(), start))
        #    start = package.getPackageAddress()
        #print('Distance:', self.getDistanceBetween(start, startingPoint))
        for package in self.truck2Packages:
           print('Package ID:', package.getPackageID())

    def getT1Distance(self):
        return self.traveledT1

    def getT2Distance(self):
        return self.traveledT2

    def getTotalDistance(self):
        distance = 0
        for d in self.truck1Distances:
            distance += d

        for d in self.truck2Distances:
            distance += d

        return distance

    def getTruck1Distance(self):
        return self.truck1Distances

    def getTruck2Distance(self):
        return self.truck2Distances

    def checkDuplicates(self):
        duplicates = []
        for package in self.truck1Packages:
            if package.getPackageID() in duplicates:
                print('Broken:', package.getPackageID())
                return None
            else:
                duplicates.append(package.getPackageID())

        duplicates = []
        for package in self.truck2Packages:
            if package.getPackageID() in duplicates:
                print('Broken')
                return None
            else:
                duplicates.append(package.getPackageID())

        print('no duplicates')

    def sortTruckPackages(self, startingPoint):
        sorted = []
        package = self.truck1Packages[0]
        sorted.append(package)
        self.truck1Packages.remove(package)
        start = package.getPackageAddress()
        for pack in self.truck1Packages:
            package = self.getMinDistance(start, self.truck1Packages, sorted, 'yes')
            sorted.append(package)
            start = package.getPackageAddress()
        self.truck1Packages = sorted



