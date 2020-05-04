import heapq
from threading import Thread, Event, Lock
from time import sleep
from operator import itemgetter

# Kunde Typ 1       interStation    Schlange zu lang    wie viel kaufen
# Baecker               10s             10                   10
# Wurst                 30s             10                   5
# Kaese                 45s             5                    3
# Kasse                 60s             20                   30

# Kunde Typ 2
# Wurst                 30s             5                    2
# Kasse                 30s             20                   3
# Baecker               20s             20                   3
#                        145


# Baecker   per article     10s
# Wurst     per article     30s
# Kaese     per article     60s
# Kasse     per article     5s

newTyp1 = 1
newTyp2 = 1
transactionList = []
fullyServedCustomers = 0
printLock = Lock()
customerCount = 0


class Kunde(Thread):

    def __init__(self, name, id):
        Thread.__init__(self)
        self.name = name
        self.waitToBeServedEv = Event()
        self.hasBeenFullyServed = True
        if id == 1:
            self.nochBesuchendeStationen = [(10, 10, 10),  # Baecker
                                            (30, 10, 5),  # Wurst
                                            (45, 5, 3),  # Kaese
                                            (60, 20, 30)]  # Kasse
            self.nochBesuchen = [0, 1, 2, 3]
        else:
            self.nochBesuchendeStationen = [(20, 20, 3),  # Baecker
                                            (30, 5, 2),  # Wurst
                                            (0, 0, 0),  # Kaese
                                            (30, 20, 3)]  # Kasse
            self.nochBesuchen = [1, 3, 0]

        self.nextStation = 0

    def goToStation(self):
        self.nextStation = self.nochBesuchen.pop(0)
        print("customer: " + self.name + " goes to Station " + stations[self.nextStation].name + ".")

        ownSleep(self.nochBesuchendeStationen[self.nextStation][0])

    def arriveAtStation(self):
        currentStation = stations[self.nextStation]


        if currentStation.ownArrEv.is_set():
            if len(currentStation.warteSchlange) < self.nochBesuchendeStationen[self.nextStation][1]:
                print("customer: " + self.name + " queues at Station " + stations[self.nextStation].name + ".")
                currentStation.warteSchlange.append(self)
                self.waitToBeServedEv.wait()


            else:
                print("customer: " + self.name + " skips Station " + stations[self.nextStation].name + ".")
                currentStation.skipStationCount = currentStation.skipStationCount + 1
                self.hasBeenFullyServed = False

                return

        self.startStation()

    def startStation(self):

        currentStation = stations[self.nextStation]
        print("customer: " + self.name + " started at Station " + currentStation.name + ".")

        currentStation.serveTimeForNextCustomer = currentStation.timePerProduct * \
                                                  self.nochBesuchendeStationen[self.nextStation][2]

        currentStation.ownArrEv.set()

        print("customer: " + self.name + " is being served " + currentStation.name + ".")
        currentStation.ownServEv.wait()

        print("customer: " + self.name + " finished at Station " + currentStation.name + ".")


    def run(self):
        print("customer: " + self.name + " arrived at the shop.")
        global customerCount
        customerCount = customerCount + 1

        # transactionList.append((globalTimeCounter, self.name, "Start", self.hasBeenFullyServed))
        startTime = globalTimeCounter
        while len(self.nochBesuchen) > 0:
            self.goToStation()
            self.arriveAtStation()

        if self.hasBeenFullyServed:
            global fullyServedCustomers
            fullyServedCustomers = fullyServedCustomers + 1

        # transactionList.append((globalTimeCounter, self.name, "Finished", self.hasBeenFullyServed))
        endTime = globalTimeCounter
        timeNeeded = endTime - startTime
        if self.hasBeenFullyServed:
            transactionList.append((self.name, timeNeeded, endTime))
        print("customer: " + self.name + " finished shopping")


class Station(Thread):

    def __init__(self, name, timePerProduct):
        print(name + " started to init.")
        Thread.__init__(self)
        self.name = name
        self.timePerProduct = timePerProduct
        self.serveTimeForNextCustomer = 0
        self.skipStationCount = 0

        self.warteSchlange = []
        self.bedientGerade = False
        self.ownArrEv = Event()
        self.ownServEv = Event()
        self.nextInQueue = Event()

    def waitForCustomer(self):
        while not globalStationStopEvent.is_set():
            self.ownArrEv.wait(timeout=SLEEP_INTERVAL)
            if self.ownArrEv.is_set():
                return

        print(self.name + " exited by Event.")
        exit(11)

    def serve(self):
        print("station: " + self.name + " started to serve.")
        ownSleep(self.serveTimeForNextCustomer)
        print("station: " + self.name + " finished to serve.")
        self.ownServEv.set()

        self.ownServEv.clear()

    def run(self):
        print(self.name + " started")

        while True:
            self.waitForCustomer()
            self.serve()

            while len(self.warteSchlange) > 0:
                nextCustomer = self.warteSchlange.pop(0)
                nextCustomer.waitToBeServedEv.set()
                nextCustomer.waitToBeServedEv.clear()

                self.serve()

            self.ownArrEv.clear()



SLEEP_INTERVAL = 0.002
GEN_TIME = 1800
SIMULATION_LENGTH = 3100
globalTimeCounter = 0


def ownSleep(howLong):
    until = globalTimeCounter + howLong
    while until > globalTimeCounter:
        sleep(SLEEP_INTERVAL / 3)
    return


def startCustomer(name, typ):
    kunde = Kunde(name, typ)
    kunde.start()


globalStationStopEvent = Event()

stations = [Station("Baecker", 10),
            Station("Wurst", 30),
            Station("Kaese", 60),
            Station("Kasse", 5)]

for stat in stations:
    stat.start()

#startCustomer("1-Typ1", 1)

print("main: started to sleep")

for i in range(0, SIMULATION_LENGTH):
    print("CurrentTime: " + str(globalTimeCounter))
    if (globalTimeCounter % 200) == 0 and globalTimeCounter < GEN_TIME:
        startCustomer(str(newTyp1) + "-Typ1", 1)
        newTyp1 = newTyp1 + 1
    if (globalTimeCounter % 60) == 1 and globalTimeCounter < GEN_TIME:
        startCustomer(str(newTyp2) + "-Typ2", 2)
        newTyp2 = newTyp2 + 1

    # if globalTimeCounter == 3:
    #    startCustomer("2-Typ1", 1)
    # if globalTimeCounter == 5:
    #    startCustomer("3-Typ1", 1)
    sleep(SLEEP_INTERVAL)
    globalTimeCounter = globalTimeCounter + 1



print("main: stopping all stations")
globalStationStopEvent.set()

(customer, timeNeede, endTime) = transactionList.pop()
transactionList.append((customer, timeNeede, endTime))

# Last customer exited the shop
lastShopper = max(transactionList, key=itemgetter(2))

# How long full shopping takes
customerFullyServedCount = len(transactionList)
customerShoppingTimeSum = 0
for i in range(len(transactionList)):
    (customerName, timeTaken, endTime) = transactionList.pop(0)
    transactionList.append((customerName, timeTaken, endTime))
    customerShoppingTimeSum = customerShoppingTimeSum + timeTaken

print("\tLast Station Serving: " + str(endTime) + "\tfrom customer: " + customer)

print("\tAnzahl Kunden: " + str(customerCount))

print("\tCustomers fully served: " + str(len(transactionList)))

print("\tEvery Customer needed approx: " + str(customerShoppingTimeSum / customerFullyServedCount) + " seconds")

# How many % of customers skipped the station
for station in stations:
    print("\t\tAt " + station.name + " " + str((station.skipStationCount / customerCount) * 100)[0:4] + " % skipped.")

print("\n")

sleep(2)
print("main: killing main")
exit(11)
