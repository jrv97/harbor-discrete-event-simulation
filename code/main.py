__author__ = 'Jorge Rodríguez de la Vega, C-412'

import matplotlib.pyplot as plt
from math import sqrt
from sys import argv
from termcolor import colored

from rv_generators import estimate_mu, estimate_sigma
from simulation import Simulation


def visualize_results(arrivals, berthing, deberthing, load_times, solotrip):
    colors = ['skyblue', 'green', 'blue']
    lists = [
        (arrivals, 'Arrival times ~ Exp($\lambda = 8$)'),
        (berthing, 'Berthing times ~ Exp($\lambda = 2$)'),
        (deberthing, 'Deberthing times ~ Exp($\lambda = 1$)'),
        (load_times[0],
            'S-tankers times~N($\mu = 9, \sigma^2 = 1$)'),
        (load_times[1],
            'M-tankers times~N($\mu = 12, \sigma^2 = 2$)'),
        (load_times[2],
            'L-tankers times~N($\mu = 18, \sigma^2 = 3$)')
    ]
    fig, ax = plt.subplots(3, 2)
    i = 0
    for row in ax:
        for col in row:
            col.hist(lists[i][0], bins='auto',
                     color=colors[i % len(colors)])
            col.set_title(lists[i][1])
            col.grid()
            i += 1
    plt.subplots_adjust(wspace=.5, hspace=1)
    plt.savefig('Pictures/Random Variables Subplots', format='png')
    plt.show()
    plt.close()
    lists.append(
        (solotrip, 'Tugboat solo trips times ~ Exp($\lambda = 0.25$)'))
    for l in lists:
        plt.hist(l[0], bins='auto')
        plt.title(l[1])
        plt.grid()
        plt.savefig('Pictures/'+l[1], format='png')
        plt.show()
        plt.close()


def main_loop(d):
    if len(argv) == 2:
        max_duration_of_simulation = argv[1]
    else:
        max_duration_of_simulation = 24

    colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']
    arrivals, berthing, deberthing, solotrip, data = [], [], [], [], []
    load_times = [[], [], []]
    sum, total = 0, 0

    for i in range(30):
        # generate 30 values for data
        sim = Simulation(max_duration_of_simulation)
        arrivals += sim.state.rv_arrivals
        berthing += sim.state.rv_berthing
        deberthing += sim.state.rv_deberthing
        load_times[0] += sim.state.rv_load_times[0]
        load_times[1] += sim.state.rv_load_times[1]
        load_times[2] += sim.state.rv_load_times[2]
        solotrip += sim.state.rv_solotrip
        sum += sim.sum
        total += sim.total

        data.append(sim.average)

        # pretty printing
        msg = """Simulation #%d | Sum: %d | Total: %d | Average: %f""" % (
            i, sim.sum, sim.total, sim.average)
        msg = colored(msg, colors[i % len(colors)])
        print(msg)
        sim.display_times()
        print('\n')

    # find k
    S = estimate_sigma(data)
    k = len(data)
    while S/sqrt(k) >= d:
        sim = Simulation(max_duration_of_simulation)

        arrivals += sim.state.rv_arrivals
        berthing += sim.state.rv_berthing
        deberthing += sim.state.rv_deberthing
        load_times[0] += sim.state.rv_load_times[0]
        load_times[1] += sim.state.rv_load_times[1]
        load_times[2] += sim.state.rv_load_times[2]
        solotrip += sim.state.rv_solotrip
        sum += sim.sum
        total += sim.total

        data.append(sim.average)
        S = estimate_sigma(data)
        k = len(data)

        # pretty printing
        msg = """Simulation #%d | Sum: %d | Total: %d | Average: %f""" % (
            k, sim.sum, sim.total, sim.average)
        msg = colored(msg, colors[k % len(colors)])
        print(msg)
        sim.display_times()
        print('\n')

    theta = estimate_mu(data)

    msg = """Total simulations: %d | Total wait time: %d | Total ships: %d | Estimated average: %f""" % (
        k, sum, total, theta)
    msg = colored(msg, colors[(k+1) % len(colors)])
    print(msg)

    visualize_results(arrivals, berthing, deberthing, load_times, solotrip)

    return theta, k


main_loop(.5)
