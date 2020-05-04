import heapq
import itertools

# Kunde Typ 1       interStation    Schlange zu lang    wie viel kaufen
# Baecker               10s             10                   10
# Wurst                 30s             10                   5
# Kaese                 45s             5                    3
# Kasse                 60s             20                   30

# Kunde Typ 2
# Wurst                 30s             5                    2
# Kasse                 30s             20                   3
# Baecker               20s             20                   3

# Baecker   per article     10s
# Wurst     per article     30s
# Kaese     per article     60s
# Kasse     per article     5s

# Tuple for EventQueue
#       time, priority, number, function, opt(args)

eventNumber = itertools.count()
globalTimeCounter = 0
customerStartEndTimes = []
customerCount = 0


# TODO next(eventNumber)

class Kunde:

    def __init__(self, name, typId, startTime):
        self.name = name
        self.nextStation = []
        self.hasBeenFullyServed = True
        self.startTime = startTime
        if typId == 1:
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

    def startShopping(self, argsList):
        global customerCount
        customerCount = customerCount + 1
        print(self.name + " startet shopping at " + str(globalTimeCounter))
        return self.goToStation([])

    def goToStation(self, argsList):
        self.nextStation = self.nochBesuchen.pop(0)

        return [[globalTimeCounter + self.nochBesuchendeStationen[self.nextStation][0], \
                 3, \
                 next(eventNumber), \
                 self.arriveAtStation, \
                 [self.nextStation]]]

    def arriveAtStation(self, argList):
        currentStationIndex = argList[0]
        currentStation = stations[currentStationIndex]

        if len(currentStation.warteSchlange) < self.nochBesuchendeStationen[currentStationIndex][1]:
            if currentStation.bedientGerade:
                print(self.name + " queues at Station " + stations[argList[0]].name + " at time " + str(
                    globalTimeCounter))
                currentStation.warteSchlange.append(self)
            else:
                return self.startStation(argList)
        else:
            self.hasBeenFullyServed = False
            currentStation.customersThatSkippedCount = currentStation.customersThatSkippedCount + 1
            return self.goToStation(argList)

    def startStation(self, argList):
        print(self.name + " starts Station " + stations[argList[0]].name + " at time " + str(globalTimeCounter))

        currentStation = argList[0]
        stations[currentStation].bedientGerade = True

        perProduct = stations[currentStation].abarbeitungsDauer

        return [[globalTimeCounter + (perProduct * self.nochBesuchendeStationen[currentStation][2]), \
                 1, \
                 next(eventNumber), \
                 self.finishedAtStation, \
                 [currentStation]]]

    def finishedAtStation(self, argList):

        print(self.name + " finished Station " + stations[argList[0]].name + " at time " + str(globalTimeCounter))
        stations[argList[0]].bedientGerade = False

        nextCustomerInQueueEvent = []
        if len(stations[argList[0]].warteSchlange) > 0:
            currentUser = stations[argList[0]].warteSchlange.pop(0)
            tempList = currentUser.startStation([currentUser.nextStation])
            for x in tempList:
                for y in x:
                    nextCustomerInQueueEvent.append(y)

        if len(self.nochBesuchen) == 0:
            customerStartEndTimes.append((self.name, globalTimeCounter - self.startTime, globalTimeCounter))
            print(self.name + " finished shopping at " + str(globalTimeCounter))
            # TODO do not end the simulation if one customer is done
            return [[-1, 10, 0, None, []]]

        retVal = self.goToStation([])
        retVal.append(nextCustomerInQueueEvent)
        return retVal


class Station:
    def __init__(self, name, abarbeitungsDauer):
        self.name = name
        self.abarbeitungsDauer = abarbeitungsDauer
        self.warteSchlange = []
        self.bedientGerade = False
        self.customersThatSkippedCount = 0


class EventQueue:
    #       time, priority, number, function, opt(args)

    def __init__(self):
        self.queue = []
        self.time = 0
        self.eventCount = 0

    def push(self, event):
        heapq.heappush(self.queue, event)

    def pop(self):
        # returns Event
        return heapq.heappop(self.queue)

    def start(self):
        global eventNumber

        kunde1 = Kunde("1 Typ1", 1, 0)
        self.push([0, 5, next(eventNumber), kunde1.startShopping, []])

        kunde2 = Kunde("1 Typ2", 2, 1)
        self.push([1, 5, next(eventNumber), kunde2.startShopping, []])

        kunde2 = Kunde("2 Typ2", 2, 61)
        self.push([61, 5, next(eventNumber), kunde2.startShopping, []])

        kunde2 = Kunde("3 Typ2", 2, 121)
        self.push([121, 5, next(eventNumber), kunde2.startShopping, []])

        kunde2 = Kunde("4 Typ2", 2, 181)
        self.push([181, 5, next(eventNumber), kunde2.startShopping, []])

        kunde2 = Kunde("2 Typ1", 1, 200)
        self.push([200, 5, next(eventNumber), kunde2.startShopping, []])

        # TODO watch out for maxtime while trouble
        #   add max eventcount
        #   add max Time
        while len(self.queue) > 0:
            global globalTimeCounter

            time, priority, eventNumber2, function, args = self.pop()

            if time == -1 and len(self.queue) == 0:
                print("The End has been reached")
                return

            elif time == -1:
                continue

            elif globalTimeCounter < time:
                globalTimeCounter = globalTimeCounter + 1
                self.push([time, priority, eventNumber2, function, args])
                continue

            else:
                tmp = function(args)

                if tmp is not None:
                    for lst in tmp:
                        if len(lst) != 0:
                            self.push([lst[0], lst[1], lst[2], lst[3], lst[4]])

                globalTimeCounter = globalTimeCounter + 1


eventQ = EventQueue()

stations = [Station("Baecker", 10),
            Station("Wurst", 30),
            Station("Kaese", 60),
            Station("Kasse", 5)]

eventQ.start()

# When last customer was served
(customerName, timeTaken, endTime) = customerStartEndTimes.pop()
customerStartEndTimes. append((customerName, timeTaken, endTime))

print("Last customer served at time: " + str(endTime))

# How much have been fully Served
print("Customers fully served " + str(len(customerStartEndTimes)))

# How long full shopping takes
customerFullyServedCount = len(customerStartEndTimes)
customerShoppingTimeSum = 0

for i in range(len(customerStartEndTimes)):
    (customerName, timeTaken, endTime) = customerStartEndTimes.pop(0)
    customerStartEndTimes.append((customerName, timeTaken, endTime))
    customerShoppingTimeSum = customerShoppingTimeSum + timeTaken

print("Every Customer needed approx " + str(customerShoppingTimeSum/customerFullyServedCount))

# percentage that skipped

for station in stations:
    print("At " + station.name + " " + str((station.customersThatSkippedCount/customerCount) * 10) + "% skipped.")




