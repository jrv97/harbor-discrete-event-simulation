__author__ = 'Jorge Rodríguez de la Vega, C-412'

from heapq import heappop, heappush

from generators import *
from ships import Tanker
from functools import total_ordering


@total_ordering
class Event:
    def __init__(self, time):
        self.time = time
        self.ended = False

    def handle(self):
        # abstract method
        pass

    def get_available_dock(self, docks):
        for i in range(len(docks)):
            if docks[i] == None:
                return i
            return -1

    def __eq__(self, other):
        return self.time == other.time

    def __lt__(self, other):
        return self.time < other.time


class Tanker_Arrival(Event):
    def __init__(self, time):
        super().__init__(time)
        self.name = 'Tanker arrival'

    def handle(self, system_state):
        # system state variables
        harbor_queue = system_state.harbor_queue
        # docks_queue = system_state.docks_queue
        events = system_state.events
        docks = system_state.docks
        dock_available = self.get_available_dock(docks)
        tugboat = system_state.tugboat
        arrivals = system_state.ships_arrivals
        # departures = system_state.ships_departures
        duration = system_state.duration

        if system_state.current_time <= duration:
            tanker_id = len(arrivals) + 1
            arrivals.append((tanker_id, self.time))
            if dock_available != None and len(harbor_queue) == 0 and tugboat.state == 'in harbor':
                # a dock is available, no tankers are in queue and the tugboat is available at harbor
                tugboat_event = Tugboat_Arrival_To_Harbor(self.time)
                tugboat.state = 'berthing'
                heappush(events, (tugboat_event.time, tugboat_event))
            # either a dock or the tugboat weren't available or the queue wasn't empty
            t = Tanker(tanker_id)
            system_state.rv_sizes[t.type] += 1
            system_state.rv_load_times[t.type].append(t.load_time)
            harbor_queue.append(t)
            arrival_t = tanker_arrival_time_generator()
            system_state.rv_arrivals.append(arrival_t)
            ev = Tanker_Arrival(self.time + arrival_t)
            heappush(events, (ev.time, ev))
        else:
            self.name = 'Tanker arrival denied due to harbor closing'
            pass


class Tugboat_Arrival_To_Harbor(Event):
    def __init__(self, time):
        super().__init__(time)
        self.name = 'Tugboat arrival to harbor'

    def handle(self, system_state):
        # system state variables
        harbor_queue = system_state.harbor_queue
        # docks_queue = system_state.docks_queue
        events = system_state.events
        docks = system_state.docks
        # dock_available = self.get_available_dock(docks)
        tugboat = system_state.tugboat
        # arrivals = system_state.ships_arrivals
        # departures = system_state.ships_departures
        tugboat.state = 'in harbor'
        if len(harbor_queue) > 0:
            # pickup a tanker and take it to the docks
            berthing_t = berthing_time_generator()
            system_state.rv_berthing.append(berthing_t)
            tugboat_event = Tugboat_Arrival_To_Dock(self.time + berthing_t)
            tugboat.state = 'berthing'
            heappush(events, (tugboat_event.time, tugboat_event))
            # tanker to be docked...
            tanker = harbor_queue.pop(0)
            a_dock = self.get_available_dock(docks)
            docks[a_dock] = tanker.id
            # generate finish loading event
            tanker_event = Tanker_Finish_Loading(
                self.time + berthing_t + tanker.load_time, a_dock)
            heappush(events, (tanker_event.time, tanker_event))
        else:
            # TODO
            pass


class Tugboat_Arrival_To_Dock(Event):
    def __init__(self, time):
        super().__init__(time)
        self.name = 'Tugboat arrival to dock'

    def handle(self, system_state):
        # system state variables
        harbor_queue = system_state.harbor_queue
        docks_queue = system_state.docks_queue
        events = system_state.events
        docks = system_state.docks
        # dock_available = self.get_available_dock(docks)
        tugboat = system_state.tugboat
        # arrivals = system_state.ships_arrivals
        # departures = system_state.ships_departures

        tugboat.state = 'in docks'
        if len(docks_queue) > 0:
            # will take the first one in line back to the harbor
            dock_id = docks_queue.pop(0)
            tanker_id = docks[dock_id]
            docks[dock_id] = None
            # move tugboat to harbor with the tanker...
            deberthing_t = deberthing_time_generator()
            system_state.rv_deberthing.append(deberthing_t)
            tugboat.state = 'deberthing'
            tugboat_event = Tugboat_Arrival_To_Harbor(self.time + deberthing_t)
            heappush(events, (tugboat_event.time, tugboat_event))
            # tanker leaves the harbor...
            tanker_event = Tanker_Departure(
                tugboat_event.time, tanker_id)
            heappush(events, (tanker_event.time, tanker_event))
        elif len(harbor_queue) > 0 and self.get_available_dock(docks) >= 0:
            # no tanker has finished loading and some tanker is waiting in harbor
            # must move tugboat alone to port
            toharbor_t = tugboat_to_harbor__time_generator()
            system_state.rv_solotrip.append(toharbor_t)
            tugboat_event = Tugboat_Arrival_To_Harbor(self.time + toharbor_t)
            tugboat.state = 'solo trip'
            heappush(events, (tugboat_event.time, tugboat_event))


class Tanker_Finish_Loading(Event):
    def __init__(self, time, dock_id):
        super().__init__(time)
        assert dock_id in [0, 1, 2]
        self.dock_id = dock_id
        self.name = 'Tanker finish loading'

    def handle(self, system_state):
        # system state variables
        # harbor_queue = system_state.harbor_queue
        docks_queue = system_state.docks_queue
        events = system_state.events
        # docks = system_state.docks
        # dock_available = self.get_available_dock(docks)
        tugboat = system_state.tugboat
        # arrivals = system_state.ships_arrivals
        # departures = system_state.ships_departures

        if len(docks_queue) == 0 and tugboat.state in ['in harbor', 'in docks']:
            travel_t = 0 if tugboat.state == 'in docks' else tugboat_to_harbor__time_generator()
            if tugboat.state == 'in docks':
                system_state.rv_solotrip.append(travel_t)
            e = Tugboat_Arrival_To_Dock(self.time + travel_t)
            tugboat.state = 'deberthing'
            heappush(events, (e.time, e))
        # more ships were in queue or the tugboat wasn't ready
        docks_queue.append(self.dock_id)


class Tanker_Departure(Event):
    def __init__(self, time, tanker_id):
        super().__init__(time)
        self.tanker_id = tanker_id
        self.name = 'Tanker departure'

    def handle(self, system_state):
        # system state variables
        # harbor_queue = system_state.harbor_queue
        # docks_queue = system_state.docks_queue
        # events = system_state.events
        # docks = system_state.docks
        # dock_available = self.get_available_dock(docks)
        # tugboat = system_state.tugboat
        # arrivals = system_state.ships_arrivals
        departures = system_state.ships_departures
        departures[self.tanker_id] = self.time
