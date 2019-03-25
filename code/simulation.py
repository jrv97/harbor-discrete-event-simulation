__author__ = 'Jorge Rodríguez de la Vega, C-412'

import matplotlib.pyplot as plt
from heapq import heappop, heappush

from events import Tanker_Arrival
from generators import tanker_arrival_time_generator
from ships import Tugboat


class Simulation:
    def __init__(self, duration):
        self.state = System_State()
        self.state.duration = duration
        # generate first arrival
        arrival_t = tanker_arrival_time_generator()
        arrival_e = Tanker_Arrival(arrival_t)
        heappush(self.state.events, (arrival_t, arrival_e))
        self.run()

    def run(self):
        # start simulation
        while len(self.state.events) > 0 and self.state.current_time <= self.state.duration:
            _, ev = heappop(self.state.events)
            ev.handle(self.state)
            self.state.current_time = ev.time
            msg = """%s occurring at % f while tugboat is % s""" % (
                ev.name, self.state.current_time, self.state.tugboat.state)
        self.sum, self.total, self.average = self.calculate_average()

    def calculate_average(self):
        total = len(self.state.ships_departures)
        sum = 0 if total != 0 else self.state.duration
        for k in self.state.ships_departures.keys():
            sum += self.state.ships_departures[k] - \
                self.state.ships_arrivals[k-1][1]
        return sum, total, sum/total if total != 0 else self.state.duration

    def display_times(self):
        for k in self.state.ships_departures.keys():
            time_a = self.state.ships_arrivals[k-1][1]
            time_d = self.state.ships_departures[k]
            msg = """|_ Tanker #%d arrived at %f and left at %f (waited %f)""" % (
                k, time_a, time_d, time_d - time_a)
            print(msg)


class System_State:
    # All simulation system status info
    def __init__(self):
        self.current_time = 0  # time of the simulation

        # arrivals[i] = (tanker_id, arrival_time) of i-th tanker
        self.ships_arrivals = []

        # departures[i] = departure time of the tanker with ID i
        self.ships_departures = {}

        self.events = []  # events heap
        self.harbor_queue = []  # ships waiting in harbor
        self.docks_queue = []  # ships waiting in docks
        self.tugboat = Tugboat()
        self.docks = [None, None, None]

        # only for r.v. analysis...
        self.rv_arrivals = []
        self.rv_sizes = [0, 0, 0]
        self.rv_load_times = [[], [], []]
        self.rv_berthing = []
        self.rv_deberthing = []
        self.rv_solotrip = []
