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


# TODO next(eventNumber)

class Kunde:

    def __init__(self, name, id):
        self.name = name
        if id == 1:
            self.nochBesuchendeStationen = [(10, 10, 10),   #Baecker
                                            (30, 10, 5),    #Wurst
                                            (45, 5, 3),     #Kaese
                                            (60, 20, 30)]   #Kasse
            self.nochBesuchen = [0, 1, 2, 3]
        else:
            self.nochBesuchendeStationen = [(20, 20, 3),    #Baecker
                                            (30, 5, 2),     #Wurst
                                            (0, 0, 0),      #Kaese
                                            (30, 20, 3)]    #Kasse
            self.nochBesuchen = [1, 3, 0]


    def startShopping(self, argsList):

        print("Customer" + self.name + " startet shopping at " + str(globalTimeCounter))
        return self.goToStation([])



    def goToStation(self, argsList):
        nextStation = self.nochBesuchen.pop(0)

        return globalTimeCounter + self.nochBesuchendeStationen[nextStation][0], \
               5, \
               next(eventNumber), \
               self.startStation, \
               [nextStation]


    def startStation(self, argList):
        print(self.name + " starts Station " + stations[argList[0]].name + " at time " + str(globalTimeCounter))

        currentStation = argList[0]

        perProduct = stations[currentStation].abarbeitungsDauer

        return globalTimeCounter + (perProduct * self.nochBesuchendeStationen[currentStation][2]),\
               5,\
               next(eventNumber),\
               self.finishedAtStation,\
               [currentStation]

    def finishedAtStation(self, argList):

        print(self.name + " finished Station " + stations[argList[0]].name + " at time " + str(globalTimeCounter))


        if len(self.nochBesuchen) == 0:
            print(self.name + " finished shopping at "  + str(globalTimeCounter))
            # TODO do not end the simulation if one customer is done
            return -1, 10, 0, None, []

        return self.goToStation([])


class Station:
    # TODO Make stations every its own instance
    def __init__(self, name, abarbeitungsDauer):
        self.name = name
        self.abarbeitungsDauer = abarbeitungsDauer
        self.warteSchlange = []
        self.bedientGerade = False

    def anstehen(self):

        return


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


        kunde1 = Kunde("1 Typ1", 1)
        kunde2 = Kunde("2 Typ1", 1)
        kunde3 = Kunde("1 Typ2", 2)

        self.push([0, 5, next(eventNumber), kunde1.startShopping, []])
        self.push([10, 5, next(eventNumber), kunde2.startShopping, []])
        # self.push([0, 5, next(eventNumber), kunde3.startShopping, []])



        # TODO watch out for maxtime while trouble
        #   add max eventcount
        #   add max Time
        while len(self.queue) > 0:
            global globalTimeCounter
            # print("Global Time: " + str(globalTimeCounter))

            time, priority, eventNumber2, function, args = self.pop()


            if time == -1:
                print("The End has been reached")
                return

            elif globalTimeCounter < time:
                globalTimeCounter = globalTimeCounter + 1
                self.push([time, priority, eventNumber2, function, args])
                continue

            else:
                a, b ,c ,d , e = function(args)
                self.push([a,b,c,d,e])
                globalTimeCounter = globalTimeCounter + 1


e = EventQueue()


stations = [Station("Baecker", 10),
            Station("Wurst", 30),
            Station("Kaese", 60),
            Station("Kasse", 5)]

e.start()
