import matplotlib.pyplot as plt
from numpy import cos, linspace, log, percentile, pi, sqrt
from random import normalvariate, random
import graphs


def exponential(lbd):
    """
    lbd -- Lambda parameter of the exponential distribution to be simulated.\n
    Simulates an exponentially distributed random variable using the Inverse Transform method.
    """
    u = random()
    return -1/lbd*log(u)


def normal(mu, sigma):
    """
    mu -- Mean of the normal distribution to be generated\n
    sigma -- Variance of the normal distribution to be generated\n
    Simulates a normally distributed random variable with mean equal to mu and variance equal to sigma using Box-Muller's method.
    """
    u1 = random()
    u2 = random()
    z = sqrt(-2.*log(u1))*cos(2.*pi*u2)
    return z*sqrt(sigma)+mu


def test_exp_dist(lbda, data_size):
    data = [exponential(lbda) for i in range(data_size)]
    lbda_e = estimate_lambda(data)
    print('Real lambda is %f, estimated %f' % (lbda, lbda_e))
    plt.hist(data, bins='auto')
    plt.grid()
    plt.title('X~Exp($\lambda=%f$)' % lbda)
    plt.show()
    plt.close()


def test_normal_dist(mu, sigma2, data_size):
    data = [normal(mu, sigma2) for i in range(data_size)]
    mu_e = estimate_mu(data)
    sigma2_e = estimate_sigma2(data)
    print('Real mu, sigma2 are %f and %f, estimated %f and %f' %
          (mu, sigma2, mu_e, sigma2_e))
    plt.hist(data, bins='auto')
    plt.grid()
    plt.title('X ~ Normal($\mu=%f,\sigma^2=%f$)' % (mu, sigma2))
    plt.show()
    plt.close()


def optimal_bins(self, data):
    # finds optimal bin width using Freedman-Diaconis rule
    q75, q25 = percentile(data, [75, 52])
    iqr = q75 - q25
    bin_width = 2*(iqr)/len(data)**1/3
    return int(bin_width)


def estimate_mu(data):
    n = len(data)
    sum = 0.0
    for i in data:
        sum += i
    return sum/n


def estimate_sigma2(data):
    n = len(data)
    sum = 0.0
    mu = estimate_mu(data)
    for i in data:
        sum += (i - mu)**2
    return sum/n-1


def estimate_sigma(data):
    return sqrt(estimate_sigma2(data))


def estimate_lambda(data):
    return 1/estimate_mu(data)


def estimate_theta(Simulation, max_duration_of_simulation, d):
    # libro de Luciano, cap. 4
    # generate 30 values for data
    data = [Simulation(max_duration_of_simulation).average for i in range(30)]
    # find k
    S = estimate_sigma(data)
    k = len(data)
    while S/sqrt(k) >= d:
        data.append(Simulation(max_duration_of_simulation).average)
        S = estimate_sigma(data)
        k = len(data)
    theta = estimate_mu(data)
    return theta, k

# testing my r.v.
# test_normal_dist(9, 1, 1000)
# test_normal_dist(12, 2, 1000)
# test_normal_dist(18, 3, 1000)
# test_exp_dist(8, 1000)
# test_exp_dist(1, 1000)
# test_exp_dist(2, 1000)
# test_exp_dist(1/4, 1000)
