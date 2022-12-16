import csv
import datetime
from package import Package
from hashTable import chainingHash
from truck import Truck

distanceData = [[0 for i in range(27)] for j in range(27)]
addressData = [None for i in range(27)]
myHash = chainingHash()


def loadPackageData(fileName):
    with open(fileName) as packageCSV:
        packageData = csv.reader(packageCSV, delimiter=',')
        for package in packageData:
            packageID = package[0]
            address = package[1]
            city = package[2]
            zipCode = package[4]
            deadline = package[5]
            weight = package[6]
            note = package[7]
            P = Package(packageID, address, deadline, city, zipCode, weight, note)
            myHash.insert(packageID, P)


def loadDistanceData(fileName):
    with open(fileName) as distanceCSV:
        distanceDataCSV = csv.reader(distanceCSV, delimiter=',')
        row = -1
        for distance in distanceDataCSV:
            row += 1
            for column in range(27):
                distanceData[row][column] = distance[column]


def loadAddressData(fileName):
    with open(fileName) as addressCSV:
        addressDataCSV = csv.reader(addressCSV, delimiter=',')
        i = 0
        for address in addressDataCSV:
            addressData[i] = address[1][1:]
            i += 1


loadPackageData('C:/Users/dakot/PycharmProjects/PAC950/CSVs/package.csv')
loadDistanceData('C:/Users/dakot/PycharmProjects/PAC950/CSVs/distance.csv')
loadAddressData('C:/Users/dakot/PycharmProjects/PAC950/CSVs/address.csv')

# print('Address:', addressData)

truck = Truck(distanceData, addressData)


startingPoint = addressData[0]
print('1st load:')
truck.loadTruck(startingPoint, myHash)
truck.checkDuplicates()

truck.deliverPackages(startingPoint, myHash)
#print('Truck 1 distances:', truck.getT1Distance())
#print('Truck 2 distance:', truck.getT2Distance())

print('second load:')
truck.loadTruck(startingPoint, myHash)
truck.checkDuplicates()

truck.deliverPackages(startingPoint, myHash)
print('T1 Distance:', truck.getT1Distance())
print('T2 Distance:', truck.getT2Distance())

# print('Hash table:', myHash.getTable())
#
print('Total Distance:', truck.getTotalDistance())

print('WGUPS Routing Program')
print('Route was completed in', truck.getTotalDistance(), 'miles')
userInput = input("""
Please select an option below to being or type 'quit' to quit:
    Type '1' to get info for all packages at a particular time
    Type '2' to get info for a single package at a particular time
""")

while userInput != 'quit':
    if userInput == '1':
        userTime = input('Enter a time in (HH:MM:SS): ')
        (hours, minutes, seconds) = userTime.split(':')
        userTime = datetime.timedelta(hours = int(hours), minutes = int(minutes), seconds = int(seconds))
        if userTime < truck.getFirstDeliveryTime():
            for i in range(1,41):
                print('Package ID:', i, ', At the hub')
        elif userTime > truck.getSecondDeliveryTime():
            for i in range(1,41):
                if myHash.search(i) in truck.getFirstTripPackages():
                    print('Package ID:', i, ',', myHash.search(i).getDeliveryStatus())

    userInput = input("""
    Please select an option below to being or type 'quit' to quit:
        Type '1' to get info for all packages at a particular time
        Type '2' to get info for a single package at a particular time
    """)


# Finished: created menu for user.
# ToDo: Make sure packages are delivered by deadline. Create UI. Finish UI ex: https://docs.python.org/3/library/datetime.html
