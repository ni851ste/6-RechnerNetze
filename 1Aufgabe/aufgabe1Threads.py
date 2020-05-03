import heapq
from threading import Thread, Event
from time import sleep

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





class Kunde(Thread):

    def __init__(self, name, id):
        Thread.__init__(self)
        self.name = name
        self.waitToBeServedEv = Event()
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
            print(self.name + " queues at Station " + stations[self.nextStation].name + ".")

            # TODO check if queue is too long
            currentStation.warteSchlange.append(self)
            self.waitToBeServedEv.wait()

        self.startStation()


    def startStation(self):
        print("customer: " + self.name + " started at Station " + stations[self.nextStation].name + ".")

        currentStation = stations[self.nextStation]
        currentStation.ownArrEv.set()

        print("customer: " + self.name + " is being served " + stations[self.nextStation].name + ".")
        currentStation.ownServEv.wait()

        print("customer: " + self.name + " finished at Station " + stations[self.nextStation].name + ".")


    #def finishedAtStation(self, argList):

    def run(self):
        print("customer: " + self.name + " started.")
        # sleep(waitAtBeginning)
        while len(self.nochBesuchen) > 0:
            self.goToStation()
            self.arriveAtStation()

        print("customer: " + self.name + " finished shopping")




class Station(Thread):
    # TODO Make stations every its own instance
    def __init__(self, name, abarbeitungsDauer, ownArrEv, ownServEv):
        print(name + " started to init.")
        Thread.__init__(self)
        self.name = name
        self.abarbeitungsDauer = abarbeitungsDauer
        self.warteSchlange = []
        self.bedientGerade = False
        self.ownArrEv = ownArrEv
        self.ownServEv = ownServEv
        self.nextInQueue = Event()

    def waitForCustomer(self):
        while not globalStationStopEvent.is_set():
            self.ownArrEv.wait(timeout=SLEEP_INTERVAL)
            if self.ownArrEv.is_set():
                return

        print(self.name + " exited by Event.")
        exit(11)


    def serve(self):
        # TODO how much articles are bought
        print("station: " + self.name + " started to serve.")
        ownSleep(self.abarbeitungsDauer)
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



SLEEP_INTERVAL = 0.05
SIMULATION_LENGTH = 350
globalTimeCounter = 0


def ownSleep(howLong):
    until = globalTimeCounter + howLong
    while until > globalTimeCounter:
        sleep(SLEEP_INTERVAL / 3)
    return


def startCustomer(name, typ):
    kunde = Kunde(name, typ)
    kunde.start()


baeckArrEv = Event()
wurstArrEv = Event()
kaeseArrEv = Event()
kasseArrEv = Event()

baeckServEv = Event()
wurstServEv = Event()
kaeseServEv = Event()
kasseServEv = Event()

globalStationStopEvent = Event()

stations = [Station("Baecker", 10, baeckArrEv, baeckServEv),
            Station("Wurst", 30, wurstArrEv, wurstServEv),
            Station("Kaese", 60, kaeseArrEv, kaeseServEv),
            Station("Kasse", 5, kasseArrEv, kasseServEv)]

for stat in stations:
    stat.start()

startCustomer("1-Typ1", 1)

print("main: started to sleep")

for i in range(0, SIMULATION_LENGTH):
    print("CurrentTime: " + str(globalTimeCounter))

    if globalTimeCounter == 5:
        startCustomer("2-Typ1", 1)

    sleep(SLEEP_INTERVAL)
    globalTimeCounter = globalTimeCounter + 1


print("main: stopping all stations")
globalStationStopEvent.set()

sleep(2)
print("main: killing main")
exit(11)


