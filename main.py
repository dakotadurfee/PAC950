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


loadPackageData('C:/Users/peral/PycharmProjects/PAC950/CSVs/package.csv')
loadDistanceData('C:/Users/peral/PycharmProjects/PAC950/CSVs/distance.csv')
loadAddressData('C:/Users/peral/PycharmProjects/PAC950/CSVs/address.csv')

# print('Address:', addressData)

truck = Truck(distanceData, addressData)

startingPoint = addressData[0]

truck.loadTruck(startingPoint, myHash)

truck.deliverPackages(startingPoint, myHash)

truck.loadTruck(startingPoint, myHash)

truck.deliverPackages(startingPoint, myHash)
packages = myHash.getTable()
for row in packages:
    for column in row:
        print(column[1].getDeliveryStatus(), column[1].getDeliveryDeadline())
print('WGUPS Routing Program')
print('Route was completed in', truck.getTotalDistance(), 'miles')
print('First DeliveryTime:', truck.getFirstDeliveryTime())
print('Second DeliveryTime:', truck.getSecondDeliveryTime())
print('Current Time:', truck.getCurrentTime())
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
        elif truck.getFirstDeliveryTime() <= userTime < truck.getSecondDeliveryTime():
            for i in range(1,41):
                if myHash.search(i) in truck.getSecondTripPackages():
                    print('Package ID:', i, ', At the hub')
                else:
                    deliveryTime = myHash.search(i).getDeliveryStatus()[13:]
                    (hours, minutes, seconds) = deliveryTime.split(':')
                    deliveryTime = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
                    if userTime >= deliveryTime:
                        print('Package ID:', i, ',', myHash.search(i).getDeliveryStatus())
                    else:
                        print('Package ID:', i, ', en route')
        elif truck.getSecondDeliveryTime() <= userTime < truck.getCurrentTime():
            for i in range(1,41):
                if myHash.search(i) in truck.getFirstTripPackages():
                    print('Package ID:', i, ',', myHash.search(i).getDeliveryStatus())
                else:
                    deliveryTime = myHash.search(i).getDeliveryStatus()[13:]
                    (hours, minutes, seconds) = deliveryTime.split(':')
                    deliveryTime = datetime.timedelta(hours = int(hours), minutes = int(minutes), seconds = int(seconds))
                    if userTime >= deliveryTime:
                        print('Package ID:', i, ',', myHash.search(i).getDeliveryStatus())
                    else:
                        print('Package ID:', i, ', en route')
        elif userTime >= truck.getCurrentTime():
            for i in range(1,41):
                print('Package ID:', i, ',', myHash.search(i).getDeliveryStatus())
    elif userInput == '2':
        userPackage = input('Enter package ID number:')
        package = myHash.search(userPackage)
        userTime = input('Enter a time in (HH:MM:SS):')
        (hours, minutes, seconds) = userTime.split(':')
        userTime = datetime.timedelta(hours = int(hours), minutes = int(minutes), seconds = int(seconds))
        if userTime < truck.getFirstDeliveryTime():
            print('Package ID:', userPackage, ', At the hub')
        elif userTime >= truck.getCurrentTime():
            print('Package ID:', userPackage, ',', package.getDeliveryStatus())
        elif package in truck.getFirstTripPackages():
            deliveryTime = package.getDeliveryStatus()[13:]
            (hours, minutes, seconds) = deliveryTime.split(':')
            deliveryTime = datetime.timedelta(hours = int(hours), minutes = int(minutes), seconds = int(seconds))
            if truck.getFirstDeliveryTime() <= userTime < truck.getSecondDeliveryTime() and userTime >= deliveryTime:
                print('Package ID:', userPackage, ',', package.getDeliveryStatus())
            elif truck.getFirstDeliveryTime() <= userTime < truck.getSecondDeliveryTime() and userTime < deliveryTime:
                print('Package ID:', userPackage, ', en route')
            else:
                print('Package ID:', userPackage, ',', package.getDeliveryStatus())
        elif package in truck.getSecondTripPackages():
            deliveryTime = package.getDeliveryStatus()[13:]
            (hours, minutes, seconds) = deliveryTime.split(':')
            deliveryTime = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            if userTime < truck.getSecondDeliveryTime():
                print('Package ID:', userPackage, ', At the hub')
            else:
                if userTime < deliveryTime:
                    print('Package ID:', userPackage, ', en route')
                else:
                    print('Package ID:', userPackage, ',', package.getDeliveryStatus())





    userInput = input("""
    Please select an option below to being or type 'quit' to quit:
        Type '1' to get info for all packages at a particular time
        Type '2' to get info for a single package at a particular time
    """)


# Finished: finished menu for user. Created loop to show packages delivery times and packages deadlines
# ToDo: make packages be delivered before deadlines. Clean up code. Add comments ex: https://docs.python.org/3/library/datetime.html
