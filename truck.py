# Dakota Durfee
# Student ID: 005550217
from datetime import timedelta

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
        self.currentTime = timedelta(hours=8)
        self.wrongAddress = timedelta(hours=10, minutes=20)
        self.addressChanged = False
        self.firstDeliveryTime = timedelta(hours=8)
        self.secondDeliveryTime = None
        self.firstTripPackages = []
        self.secondTripPackages = []
        self.T1SecondTrip = []
        self.T2SecondTrip = []

    # This method returns the distance between two addresses
    def getDistanceBetween(self, address1, address2):

        d = self.distanceData[self.addressData.index(address1)][self.addressData.index(address2)]
        if d == '':
            d = self.distanceData[self.addressData.index(address2)][self.addressData.index(address1)]

        return float(d)

    # This method uses the nearest neighbor approach to find the next package to be loaded or delivered. It starts with
    # a package object, a distance and a starting point which would be the hub. It loops through every package and assigns
    # the package object to the current package if the distance from the starting point to the delivery address is shorter
    # than the already assigned distance. It will set the new starting point as the package's delivery address, and update
    # the distance. The package with the closest delivery address from the starting point is returned.
    def getMinDistance(self, startingPoint, packages, exclude=None, altSearch='no'):
        distance = 50
        pack = Package()
        start = startingPoint

        # This case has a space-time complexity of O(n^2)
        if altSearch == 'no':
            for package in packages:
                for p in package:
                    if p[1].getDeliveryStatus() == 'at the hub':
                        if p[1].getPackageAddress() != start and exclude is None:
                            if float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())) < float(
                                    distance):
                                pack = p[1]
                                distance = self.getDistanceBetween(startingPoint, p[1].getPackageAddress())
                        elif exclude is not None and p[1] not in exclude and p[1].getPackageAddress() != start:
                            if float(self.getDistanceBetween(startingPoint, p[1].getPackageAddress())) < float(
                                    distance):
                                pack = p[1]
                                distance = self.getDistanceBetween(start, p[1].getPackageAddress())
        # This case has a space-time complexity of O(n)
        elif altSearch == 'yes':
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
        # This case has a space-time complexity of O(n)
        else:
            for package in packages:
                if float(self.getDistanceBetween(start, package.getPackageAddress())) < float(distance):
                    pack = package
                    distance = self.getDistanceBetween(start, package.getPackageAddress())
        return pack

    # This method tries to optimally load each truck. The only package that is manually loaded is package ID: 34.
    # This package is manually loaded to ensure each package is delivered by their deadline.
    def loadTruck(self, startingPoint, hashMap):
        start = startingPoint
        buddyPackages = []
        self.numLoads += 1
        # This loop appends packages that must be delivered together to the buddyPackages list so that list can later
        # be loaded onto a truck.
        # space-time complexity is O(n^2)
        for row in hashMap.getTable():
            for column in row:
                note = column[1].getPackageNote()
                if note[:22] == 'Must be delivered with':
                    buddyPackages.append(column[1])
                    if hashMap.search(note[23:25]) not in buddyPackages:
                        buddyPackages.append(hashMap.search(note[23:25]))
                    elif hashMap.search(note[26:]) not in buddyPackages:
                        buddyPackages.append(hashMap.search(note[26:]))

        # The code in this if statement executes if this is for the first delivery trip.
        if self.numLoads <= 1:
            self.truck1Packages.append(hashMap.search('34'))
            self.firstTripPackages.append(hashMap.search('34'))
            hashMap.search('34').setDeliveryStatus('en route')

            # Loops until the maximum allowed amount of packages are loaded on truck 1.
            while len(self.truck1Packages) < 16:
                package = self.getMinDistance(start, hashMap.getTable())
                exclude = []
                # Loops until a package at the hub is found.
                while package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                    start = package.getPackageAddress()
                exclude = []

                # Loops until a package that can be loaded on truck 1 and is not delayed is found.
                while package.getPackageNote() == 'Can only be on truck 2' or package.getPackageNote()[
                                                                              :7] == 'Delayed' or package.getPackageNote()[
                                                                                                  :5] == 'Wrong' or package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                # Assures all packages that must be delivered together are on the same truck.
                if package in buddyPackages:
                    self.truck1Packages.append(package)
                    self.firstTripPackages.append(package)
                    buddyPackages.remove(package)
                    package.setDeliveryStatus('en route')
                    while len(buddyPackages) > 0:
                        package = self.getMinDistance(start, buddyPackages, None, 'yes')
                        self.truck1Packages.append(package)
                        self.firstTripPackages.append(package)
                        buddyPackages.remove(package)
                        package.setDeliveryStatus('en route')
                        start = self.truck1Packages[-1].getPackageAddress()
                elif package.getPackageNote() == '':
                    self.truck1Packages.append(package)
                    self.firstTripPackages.append(package)
                    start = package.getPackageAddress()
                    package.setDeliveryStatus('en route')

            # Assigns the starting point as the hub address so truck 2 can be more optimally loaded.
            start = startingPoint
            # Loops until the maximum allowed amount of packages are loaded on truck 2.
            while len(self.truck2Packages) < 16:

                package = self.getMinDistance(start, hashMap.getTable())
                # Loops until a package at the hub is found.
                while package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                exclude = []

                # Loops until a package that is not delayed is found.
                while package.getPackageNote()[:7] == 'Delayed' or package.getPackageNote()[
                                                                   :5] == 'Wrong' or package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                self.truck2Packages.append(package)
                self.firstTripPackages.append(package)
                start = package.getPackageAddress()
                package.setDeliveryStatus('en route')

        else:
            self.secondDeliveryTime = self.currentTime
            # space-time complexity O(n^2)
            for row in hashMap.getTable():
                for column in row:
                    # Assures all packages are loaded on the correct truck.
                    if column[1].getPackageNote() == 'Can only be on truck 2' and column[
                        1].getDeliveryStatus() == 'at the hub':
                        self.truck2Packages.append(column[1])
                        self.secondTripPackages.append(column[1])
                        column[1].setDeliveryStatus('en route')
                        start = column[1].getPackageAddress()
            # After the first trip there are only 8 packages remaining at the hub so each truck can take 4 packages.
            # Loops until 4 packages are loaded on truck 2.
            while len(self.truck2Packages) < 4:
                package = self.getMinDistance(start, hashMap.getTable())
                exclude = []
                while package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                self.truck2Packages.append(package)
                self.secondTripPackages.append(package)
                package.setDeliveryStatus('en route')
                start = package.getPackageAddress()

            # Loops until 4 packages are loaded on truck 1.
            while len(self.truck1Packages) < 4:
                package = self.getMinDistance(start, hashMap.getTable())
                while package.getDeliveryStatus() != 'at the hub':
                    exclude.append(package)
                    package = self.getMinDistance(start, hashMap.getTable(), exclude)
                self.truck1Packages.append(package)
                self.secondTripPackages.append(package)
                package.setDeliveryStatus('en route')
                start = package.getPackageAddress()

    # This method optimally delivers the packages loaded on trucks 1 and 2. It also keeps track of the time it takes for
    # each truck to complete its route and the distance each truck traveled.
    def deliverPackages(self, startingPoint, hashMap):
        start = startingPoint
        # Keeps track of how long it takes for both trucks to complete their routes.
        T1TravelTime = timedelta(hours=0)
        T2TravelTime = timedelta(hours=0)
        # Loops until all packages on truck 1 are delivered.
        while len(self.truck1Packages) > 0:
            # Updates the package that initally had the wrong address listed to the correct delivery address. The update
            # happens after WGU finds the correct address.
            if (self.currentTime + T1TravelTime) > self.wrongAddress and self.addressChanged == False:
                pack = hashMap.search('9')
                pack.setPackageAddress('410 S State St')
                self.addressChanged = True
            package = self.getMinDistance(start, self.truck1Packages, None, 'delivery')
            distance = self.getDistanceBetween(start, package.getPackageAddress())
            self.traveledT1 += distance
            T1TravelTime += self.timeToDeliver(distance)
            self.truck1Packages.remove(package)
            deliveryTime = 'Delivered at ' + str(self.currentTime + T1TravelTime)
            package.setDeliveryStatus(deliveryTime)
            start = package.getPackageAddress()

        # Records the time and distance it takes to get from the last package delivered on truck 1 back to the hub.
        self.traveledT1 += self.getDistanceBetween(start, startingPoint)
        T1TravelTime += self.timeToDeliver(distance)
        start = startingPoint

        # Loops until all packages on truck 2 are delivered.
        while len(self.truck2Packages) > 0:
            package = self.getMinDistance(start, self.truck2Packages, None, 'delivery')
            distance = self.getDistanceBetween(start, package.getPackageAddress())
            self.traveledT2 += distance
            T2TravelTime += self.timeToDeliver(distance)
            self.truck2Packages.remove(package)
            deliveryTime = 'Delivered at ' + str(self.currentTime + T2TravelTime)
            package.setDeliveryStatus(deliveryTime)
            start = package.getPackageAddress()

        # Records the time and distance
        self.traveledT2 += self.getDistanceBetween(start, startingPoint)
        T2TravelTime += self.timeToDeliver(distance)

        # Changes the global time based off which truck took longer to deliver it's packages.
        if T1TravelTime > T2TravelTime:
            self.currentTime += T1TravelTime
        else:
            self.currentTime += T2TravelTime

    # Returns the total distance traveled by both trucks.
    def getTotalDistance(self):
        return self.traveledT1 + self.traveledT2

    # Returns the time it takes the trucks to go a given distance.
    def timeToDeliver(self, distance):
        time = timedelta(hours=distance / 18)
        return time

    # Returns the time
    def getCurrentTime(self):
        return self.currentTime

    # Returns the time the first delivery trip starts.
    def getFirstDeliveryTime(self):
        return self.firstDeliveryTime

    # Returns the time the second delivery trip starts.
    def getSecondDeliveryTime(self):
        return self.secondDeliveryTime

    # Returns a list of packages that were delivered on the first trip.
    def getFirstTripPackages(self):
        return self.firstTripPackages

    # Returns a list of packages that were delivered on the second trip.
    def getSecondTripPackages(self):
        return self.secondTripPackages
