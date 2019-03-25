__author__ = 'Jorge Rodríguez de la Vega, C-412'

from random import random

from rv_generators import exponential, normal


def tanker_arrival_time_generator():
    """
    Generates the time of a tanker arrival. It is known that any arrival ~ Exp(8).
    """
    return exponential(8)


def tanker_size_generator():
    """
    Generates any of the possible 3 types of tankers: 0 for small, 1 for medium and 2 for big with proability 0.25, 0.25 and 0.5 respectively.
    """
    u = random()
    if u <= .25:
        return 0
    if u <= .5:
        return 1
    return 2


def tanker_load_time_generator(tanker_size):
    """
    Generates the load time for a given tanker size. It is known that the load time ~ Normal(mu, sigma).
    """
    if tanker_size == 0:  # small
        return normal(9, 1)
    if tanker_size == 1:  # medium
        return normal(12, 2)
    return normal(18, 3)  # big


def berthing_time_generator():
    """
    Time it takes for the tugboat to move a tanker from the harbor to the docks.
    """
    return exponential(2)


def deberthing_time_generator():
    """
    Time it takes for the tugboat to move a tanker from the docks to the harbor.
    """
    return exponential(1)


def tugboat_to_harbor__time_generator():
    """
    Time it takes the tugboat to go alone from the harbor to the docks.
    """
    return exponential(1/4)
