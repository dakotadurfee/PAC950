from hashTable import chainingHash
from package import Package
from datetime import timedelta


class Truck:
    def __init__(self, distanceData, addressData):
        self.truck1Packages = []
        self.truck2Packages = []
        self.distanceData = distanceData
        self.addressData = addressData
        self.traveledT1 = 0
        self.traveledT2 = 0
        self.numLoads = 0
        self.currentTime = timedelta(hours=8)
        self.wrongAddress = timedelta(hours=10, minutes=20)
        self.addressChanged = False
        self.firstDeliveryTime = timedelta(hours=8)
        self.secondDeliveryTime = None
        self.firstTripPackages = []
        self.secondTripPackages = []
        self.T1SecondTrip = []
        self.T2SecondTrip = []

    def getDistanceBetween(self, address1, address2):

        d = self.distanceData[self.addressData.index(address1)][self.addressData.index(address2)]
        if d == '':
            d = self.distanceData[self.addressData.index(address2)][self.addressData.index(address1)]

        return float(d)

    def getMinDistance(self, startingPoint, packages, exclude=None, buddyPackages='no'):
        distance = 50
        pack = Package()
        start = startingPoint

        if buddyPackages == 'no':
            for package in packages:
                for p in package:
                    if p[1].getDeliveryStatus() == 'at the hub':
                        if p[1].getPackageAddress() != start and exclude is None:
                            # print('package:', p[1].getPackageAddress())

                            if float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())) < float(
                                    distance):
                                pack = p[1]
                                distance = self.getDistanceBetween(startingPoint, p[1].getPackageAddress())
                                # start = p[1].getPackageAddress()
                        elif exclude is not None and p[1] not in exclude and p[1].getPackageAddress() != start:
                            if float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())) < float(
                                    distance):
                                pack = p[1]
                                distance = self.getDistanceBetween(start, p[1].getPackageAddress())
                                # start = p[1].getPackageAddress()
        elif buddyPackages == 'yes':
            if exclude == None:
                for package in packages:
                    if package.getDeliveryStatus() == 'at the hub':
                        if float(self.getDistanceBetween(start, package.getPackageAddress())) < float(distance):
                            pack = package
                            distance = self.getDistanceBetween(start, package.getPackageAddress())

            else:
                for package in packages:
                    if package.getDeliveryStatus() == 'at the hub':
                        if package not in exclude and float(
                                self.getDistanceBetween(start, package.getPackageAddress())) < float(distance):
                            pack = package
                            distance = self.getDistanceBetween(start, package.getPackageAddress())

        else:
            for package in packages:
                if float(self.getDistanceBetween(start, package.getPackageAddress())) < float(distance):
                    pack = package
                    distance = self.getDistanceBetween(start, package.getPackageAddress())
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
            self.truck1Packages.append(hashMap.search('34'))

            while len(self.truck1Packages) < 16:
                package = self.getMinDistance(start, hashMap.getTable())
                exclude = []
                while package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                    start = package.getPackageAddress()
                exclude = []

                while package.getPackageNote() == 'Can only be on truck 2' or package.getPackageNote()[
                                                                              :7] == 'Delayed' or package.getPackageNote()[
                                                                                                  :5] == 'Wrong' or package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                if package in buddyPackages:
                    self.truck1Packages.append(package)
                    self.firstTripPackages.append(package)
                    buddyPackages.remove(package)
                    # hashMap.remove(package.getPackageID())
                    package.setDeliveryStatus('en route')
                    while len(buddyPackages) > 0:
                        package = self.getMinDistance(start, buddyPackages, None, 'yes')
                        self.truck1Packages.append(package)
                        self.firstTripPackages.append(package)
                        buddyPackages.remove(package)
                        # hashMap.remove(package.getPackageID())
                        package.setDeliveryStatus('en route')
                        start = self.truck1Packages[-1].getPackageAddress()
                elif package.getPackageNote() == '':
                    self.truck1Packages.append(package)
                    self.firstTripPackages.append(package)
                    start = package.getPackageAddress()
                    # hashMap.remove(package.getPackageID())
                    package.setDeliveryStatus('en route')

            start = startingPoint
            while len(self.truck2Packages) < 16:

                package = self.getMinDistance(start, hashMap.getTable())
                while package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                exclude = []

                while package.getPackageNote()[:7] == 'Delayed' or package.getPackageNote()[
                                                                   :5] == 'Wrong' or package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                self.truck2Packages.append(package)
                self.firstTripPackages.append(package)
                start = package.getPackageAddress()
                # hashMap.remove(package.getPackageID())
                package.setDeliveryStatus('en route')

        else:
            self.secondDeliveryTime = self.currentTime
            for row in hashMap.getTable():
                for column in row:
                    if column[1].getPackageNote() == 'Can only be on truck 2' and column[
                        1].getDeliveryStatus() == 'at the hub':
                        self.truck2Packages.append(column[1])
                        self.secondTripPackages.append(column[1])
                        column[1].setDeliveryStatus('en route')
                        start = column[1].getPackageAddress()
            while len(self.truck2Packages) < 4:
                package = self.getMinDistance(start, hashMap.getTable())
                exclude = []
                while package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                self.truck2Packages.append(package)
                self.secondTripPackages.append(column[1])
                # hashMap.remove(package.getPackageID())
                package.setDeliveryStatus('en route')
                start = package.getPackageAddress()

            while len(self.truck1Packages) < 4:
                package = self.getMinDistance(start, hashMap.getTable())
                while package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                self.truck1Packages.append(package)
                self.secondTripPackages.append(package)
                # hashMap.remove(package.getPackageID())
                package.setDeliveryStatus('en route')
                start = package.getPackageAddress()

    def deliverPackages(self, startingPoint, hashMap):
        start = startingPoint
        T1TravelTime = timedelta(hours=0)
        T2TravelTime = timedelta(hours=0)
        while len(self.truck1Packages) > 0:
            if self.currentTime > self.wrongAddress and self.addressChanged == False:
                pack = hashMap.search(9)
                pack.setPackageAddress('410 S State St')
                self.addressChanged = True
            package = self.getMinDistance(start, self.truck1Packages, None, 'delivery')
            distance = self.getDistanceBetween(start, package.getPackageAddress())
            self.traveledT1 += distance
            T1TravelTime += self.timeToDeliver(distance)
            # self.currentTime += self.timeToDeliver(distance)
            self.truck1Packages.remove(package)
            deliveryTime = 'Delivered at ' + str(self.currentTime + T1TravelTime)
            package.setDeliveryStatus(deliveryTime)
            start = package.getPackageAddress()

        self.traveledT1 += self.getDistanceBetween(start, startingPoint)
        T1TravelTime += self.timeToDeliver(distance)
        # self.currentTime += self.timeToDeliver(self.getDistanceBetween(start, startingPoint))
        start = startingPoint

        while len(self.truck2Packages) > 0:
            package = self.getMinDistance(start, self.truck2Packages, None, 'delivery')
            distance = self.getDistanceBetween(start, package.getPackageAddress())
            self.traveledT2 += distance
            T2TravelTime += self.timeToDeliver(distance)
            # self.currentTime += self.timeToDeliver(distance)
            self.truck2Packages.remove(package)
            deliveryTime = 'Delivered at ' + str(self.currentTime + T2TravelTime)
            package.setDeliveryStatus(deliveryTime)
            start = package.getPackageAddress()

        self.traveledT2 += self.getDistanceBetween(start, startingPoint)
        T2TravelTime += self.timeToDeliver(distance)
        # self.currentTime += self.timeToDeliver(self.getDistanceBetween(start, startingPoint))
        if T1TravelTime > T2TravelTime:
            self.currentTime += T1TravelTime
        else:
            self.currentTime += T2TravelTime

    def getTruck1(self, startingPoint):
        start = startingPoint
        # for package in self.truck1Packages:
        #    print('Distance:', self.getDistanceBetween(package.getPackageAddress(), start))
        #    start = package.getPackageAddress()
        # print('Distance:', self.getDistanceBetween(start, startingPoint))
        for package in self.truck1Packages:
            print('Package ID:', package.getPackageID())

    def getTruck2(self, startingPoint):
        start = startingPoint
        # for package in self.truck2Packages:
        #    print('Distance:', self.getDistanceBetween(package.getPackageAddress(), start))
        #    start = package.getPackageAddress()
        # print('Distance:', self.getDistanceBetween(start, startingPoint))
        for package in self.truck2Packages:
            print('Package ID:', package.getPackageID())

    def getT1Distance(self):
        return self.traveledT1

    def getT2Distance(self):
        return self.traveledT2

    def getTotalDistance(self):
        return self.traveledT1 + self.traveledT2

    def getT1Packages(self):
        return self.truck1Packages

    def getT2Packages(self):
        return self.truck2Packages

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

    def timeToDeliver(self, distance):
        time = timedelta(hours=distance / 18)
        return time

    def getCurrentTime(self):
        return self.currentTime

    def getFirstDeliveryTime(self):
        return self.firstDeliveryTime

    def getSecondDeliveryTime(self):
        return self.secondDeliveryTime

    def getFirstTripPackages(self):
        return self.firstTripPackages

    def getSecondTripPackages(self):
        return self.secondTripPackages
