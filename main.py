import csv
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


loadPackageData('C:/Users/peral/PycharmProjects/PAC950/CSVs/package.csv')
loadDistanceData('C:/Users/peral/PycharmProjects/PAC950/CSVs/distance.csv')
loadAddressData('C:/Users/peral/PycharmProjects/PAC950/CSVs/address.csv')

# print('Address:', addressData)

truck = Truck(distanceData, addressData)
packages = myHash.getTable()

startingPoint = addressData[0]
print('1st load:')
truck.loadTruck(startingPoint, myHash)
pack = truck.getPackages()

truck.checkDuplicates()

packs = truck.getPackages()

truck.deliverPackages(startingPoint)

print('Truck 1 distances:', truck.getT1Distance())
print('Truck 2 distance:', truck.getT2Distance())

print('second load:')

truck.loadTruck(startingPoint, myHash)
truck.checkDuplicates()
packs = truck.getPackages()

# print('Truck 1 IDs:')
# truck.getTruck1(startingPoint)
# print('Truck 2 IDs:')
# truck.getTruck2(startingPoint)

truck.deliverPackages(startingPoint)
print('T1 Distance:', truck.getT1Distance())
print('T2 Distance:', truck.getT2Distance())

# print('Hash table:', myHash.getTable())
#
print('Total Distance:', truck.getTotalDistance())
print('truck 1 total distance:', truck.getT1Distance())
print('truck 2 total distance:', truck.getT2Distance())
# print('truck 1 distances:', truck.getTruck1Distance())
# print('truck 2 distances:', truck.getTruck2Distance())

# Finished: got total combined miles under 140.
# ToDo: check if packages with special note: "can only be loaded on truck 2" are only on truck 2. Create timedelta object to keep track of trucks and packages at specific times. ex: https://docs.python.org/3/library/datetime.html
