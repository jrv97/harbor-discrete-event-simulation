__author__ = 'Jorge Rodríguez de la Vega, C-412'

from generators import tanker_load_time_generator, tanker_size_generator


class Tanker:
    def __init__(self, id=-1):
        self.type = tanker_size_generator()
        self.load_time = tanker_load_time_generator(self.type)
        self.id = id

    def __str__(self):
        return 'Tanker #%d' % self.id


class Tugboat:
    def __init__(self):
        self.arrival_time = 0
        self.state = 'in harbor'

    def __str__(self):
        return 'Tugboat'

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, x):
        self._state = x
