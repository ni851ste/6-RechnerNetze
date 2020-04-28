from heapq import heappop, heappush, heapify


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

class Kunde:

    def __init__(self, id):
        self.id = id
        self.nochBesuchendeStationen = []
        self.bedientGerade = False


class Station:

    def __init__(self, name, abarbeitungsDauer):
        self.name = name
        self.abarbeitungsDauer = abarbeitungsDauer
        self.warteSchlange = []


class EventQueue:

    def __init__(self):
        self.queue = heapify([])

    def pop(self):
        heappop(self.queue)

    def push(self, arg):
        heappush(self.queue, arg)

    def start(self):
        kundeA1 = Kunde(1)
        print(kundeA1.id)




e = EventQueue
e.start()
