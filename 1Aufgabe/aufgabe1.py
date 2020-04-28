from heapq import heappop, heappush, heapify
import itertools

# Kunde Typ 1       interStation    Schlange zu lang    Einkauf Nummer
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


# TODO next(eventNumber)

class Kunde:

    def __init__(self, id):
        self.id = id
        if id == 1 or True:
            self.nochBesuchendeStationen = [(10, 10, 10),   #Baecker
                                            (30, 10, 5),    #Wurst
                                            (45, 5, 3),     #Kaese
                                            (60, 20, 30)]   #Kasse
            self.nochBesuchen = ["Baecker", "Kasse"]
        else:
            self.nochBesuchendeStationen = [(30, 5, 2),     #Wurst
                                            (30, 20, 3),    #Kasse
                                            (20, 20, 3)]    #Baecker

    def startShopping(self):
        # walk to Baeker
        print("Customer" + str(self.id) + " startet shopping")
        print("Customer" + str(self.id) + " finished shopping")



class Station:

    # TODO Make stations every its own instance
    def __init__(self):
        # self.name = name
        self.abarbeitungsDauer = [10, 30, 60, 5]
        self.warteSchlange = [[], [], [], []]
        self.bedientGerade = [False, False, False, False]

    def anstehen(self):

        return


class EventQueue:
    #       time, priority, number, function, opt(args)

    def __init__(self):
        self.queue = []
        self.time = 0
        self.eventCount = 0

    def push(self, event):
        heappush(self.queue, event)

    def pop(self):
        # returns Event
        time, priority, eventNumber2, function, args = heappop(self.queue)
        return time, priority, eventNumber2, function, args

    def start(self):
        kundeA1 = Kunde(1)

        self.push([0, 2, 1000, kundeA1.startShopping, []])
        next(eventNumber)

        # TODO watch out for maxtime while trouble
        #   add max eventcount
        #   add max Time
        while len(self.queue) > 0 and True:
            time, priority, eventNumber2, function, args = self.pop()
            function()
        print("The End has been reached")
        return


e = EventQueue()

e.start()
