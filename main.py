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

loadPackageData('C:/Users/dakot/PycharmProjects/PAC950/CSVs/package.csv')
loadDistanceData('C:/Users/dakot/PycharmProjects/PAC950/CSVs/distance.csv')
loadAddressData('C:/Users/dakot/PycharmProjects/PAC950/CSVs/address.csv')

#print('Address:', addressData)

truck = Truck(distanceData, addressData)
packages = myHash.getTable()
i = 0
#for row in packages:
#    for column in row:
#        print('ID:', column[1].getPackageID())
#        print('Address:', column[1].getPackageAddress())
#        i += 1

#for row in packages:
#   for column in row:
#       if column[1].getPackageNote() != '':
#           print('package ID:', column[1].getPackageID())
#           print('package Note:', column[1].getPackageNote())

startingPoint = addressData[0]
truck.loadTruck(startingPoint, myHash)

print('Truck 1:')
truck.getTruck1()
#print('Truck 2:')
#truck.getTruck2()

print('Distance:', truck.getTotalDistance())
print('truck 1 distances:', truck.getTruck1Distance())
print('truck 2 distances:', truck.getTruck2Distance())

