import csv
import datetime

from hashTable import chainingHash
from package import Package
from truck import Truck

# Initializes a 2D array to store the distances between addresses
distanceData = [[0 for i in range(27)] for j in range(27)]
# Initializes an array to store the delivery addresses
addressData = [None for i in range(27)]
myHash = chainingHash()

# This method reads in data from a csv file and creates package objects to hold that data.
def loadPackageData():
    with open('CSVs/package.csv') as packageCSV:
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

# This method fills the distanceData array with distances read in from a csv file.
def loadDistanceData():
    with open('CSVs/distance.csv') as distanceCSV:
        distanceDataCSV = csv.reader(distanceCSV, delimiter=',')
        row = -1
        for distance in distanceDataCSV:
            row += 1
            for column in range(27):
                distanceData[row][column] = distance[column]

# This method fills the addressData array with addresses read in from a csv file.
def loadAddressData():
    with open('CSVs/address.csv') as addressCSV:
        addressDataCSV = csv.reader(addressCSV, delimiter=',')
        i = 0
        for address in addressDataCSV:
            addressData[i] = address[1][1:]
            i += 1

# These call the methods to read in data from csv files.
loadPackageData()
loadDistanceData()
loadAddressData()

truck = Truck(distanceData, addressData)

# Creates the starting point so the loadTruck method knows to look for a package closest to that starting point
startingPoint = addressData[0]

# Calls method to load trucks for first delivery trip
truck.loadTruck(startingPoint, myHash)

# Calls method to deliver packages on the loaded trucks
truck.deliverPackages(startingPoint, myHash)

# Calls method to load trucks for second delivery trip
truck.loadTruck(startingPoint, myHash)

# Calls method to deliver packages on the loaded trucks.
truck.deliverPackages(startingPoint, myHash)

# This creates the UI for the WGUPS Routing Program. It shows how many miles the route took to complete and
# gives the user directions for operating the UI.
print('WGUPS Routing Program')
print('Route was completed in', truck.getTotalDistance(), 'miles')
userInput = input("""
Please select an option below to being or type 'quit' to quit:
    Type '1' to get info for all packages at a particular time
    Type '2' to get info for a single package at a particular time
    Type '3' to get the info for a single package
""")

while userInput != 'quit':
    # If the user types 1 then they are prompted to enter a time to see the status of all packages at that time.
    if userInput == '1':
        userTime = input('Enter a time in (HH:MM:SS): ')
        (hours, minutes, seconds) = userTime.split(':')
        userTime = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        # If the user entered time is before the first delivery time then the program displays all packages as 'At the hub'
        if userTime < truck.getFirstDeliveryTime():
            for i in range(1, 41):
                print('Package ID:', i, ', At the hub')
        # If user entered time is after first delivery trip time and before second delivery trip time then all packages that were
        # on the second delivery run will be marked as 'At the hub'. Packages on the first delivery run are checked
        # if they were delivered or en route at the user entered time.
        elif truck.getFirstDeliveryTime() <= userTime < truck.getSecondDeliveryTime():
            for i in range(1, 41):
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
        # If user entered time is after second delivery trip time and before the time the trucks completed their routes then
        # all packages that were on the first delivery run will be displayed with what time they were delivered. Packages on
        # the second delivery run are checked if they were delivered or en route at the user entered time.
        elif truck.getSecondDeliveryTime() <= userTime < truck.getCurrentTime():
            for i in range(1, 41):
                if myHash.search(i) in truck.getFirstTripPackages():
                    print('Package ID:', i, ',', myHash.search(i).getDeliveryStatus())
                else:
                    deliveryTime = myHash.search(i).getDeliveryStatus()[13:]
                    (hours, minutes, seconds) = deliveryTime.split(':')
                    deliveryTime = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
                    if userTime >= deliveryTime:
                        print('Package ID:', i, ',', myHash.search(i).getDeliveryStatus())
                    else:
                        print('Package ID:', i, ', en route')
        # This case is if the user entered a time after the trucks completed their routes and displays all packages and
        # what time they were delivered.
        else:
            for i in range(1, 41):
                print('Package ID:', i, ',', myHash.search(i).getDeliveryStatus())
    # If the user types '2' then they are promted to enter a package ID and a time.
    elif userInput == '2':
        userPackage = input('Enter package ID number:')
        package = myHash.search(userPackage)
        userTime = input('Enter a time in (HH:MM:SS):')
        (hours, minutes, seconds) = userTime.split(':')
        userTime = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        # If user entered time is before first trip delivery time then package is marked as 'At the hub'.
        if userTime < truck.getFirstDeliveryTime():
            print('Package ID:', userPackage, ', At the hub')
        # If user entered time is after the time the trucks completed their routes then the time the package was delivered is displayed.
        elif userTime >= truck.getCurrentTime():
            print('Package ID:', userPackage, ',', package.getDeliveryStatus())
        elif package in truck.getFirstTripPackages():
            deliveryTime = package.getDeliveryStatus()[13:]
            (hours, minutes, seconds) = deliveryTime.split(':')
            deliveryTime = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            # If user entered time is after first trip delivery time, before second trip delivery time, and after the time
            # the package was delivered then the package's delivered time is displayed.
            if truck.getFirstDeliveryTime() <= userTime < truck.getSecondDeliveryTime() and userTime >= deliveryTime:
                print('Package ID:', userPackage, ',', package.getDeliveryStatus())
            # If user entered time is after first trip delivery time, before second trip delivery time, and before the time
            # the package was delivered then the package is displayed as 'en route'.
            elif truck.getFirstDeliveryTime() <= userTime < truck.getSecondDeliveryTime() and userTime < deliveryTime:
                print('Package ID:', userPackage, ', en route')
            else:
                print('Package ID:', userPackage, ',', package.getDeliveryStatus())
        elif package in truck.getSecondTripPackages():
            deliveryTime = package.getDeliveryStatus()[13:]
            (hours, minutes, seconds) = deliveryTime.split(':')
            deliveryTime = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            # If user entered time is before second trip delivery time then the package is displayed as 'At the hub'.
            if userTime < truck.getSecondDeliveryTime():
                print('Package ID:', userPackage, ', At the hub')
            else:
                if userTime < deliveryTime:
                    print('Package ID:', userPackage, ', en route')
                else:
                    print('Package ID:', userPackage, ',', package.getDeliveryStatus())
    elif userInput =='3':
        userPackage = input('Enter package ID number:')
        package = myHash.search(userPackage)
        print('Package ID:', package.getPackageID())
        print('Package delivery address:', package.getPackageAddress())
        print('Package delivery deadline:', package.getDeliveryDeadline())
        print('Package delivery city:', package.getPackageCity())
        print('Package delivery zip code:', package.getZipCode())
        print('Package weight:', package.getWeight())
        print('Package delivery status:', package.getDeliveryStatus())

    userInput = input("""
    Please select an option below to being or type 'quit' to quit:
        Type '1' to get info for all packages at a particular time
        Type '2' to get info for a single package at a particular time
        Type '3' to get the info for a single package
    """)

