import numpy as np
import matplotlib.pyplot as plt

from scipy import special, integrate

#from hankel import HankelTransform
import hankel as hankel

# def integrand(x):
#     output = np.exp(-(x-1.0)**2.0)
#     return output
#
#
#
# solution = integrate.quad(integrand, -np.inf, np.inf)
# print(solution)


def main(k_array, a):

    def integrand(r, k, a):
        return special.jv(1, k * r) * r**a


    r_min = 1.0
    r_max = 10**5.0
    r = np.logspace(0.0, 2.0, 1000)
    for i, k in enumerate(k_array):


        plt.figure()
        plt.plot(r, integrand(r, k, a))
        plt.show()
        #exit()

    # f_int = np.zeros(
    #     shape=(len(k_array), )
    # )
    # for i, k in enumerate(k_array):
    #     print(i)
    #     f_int[i] = integrate.quad(integrand, 0, np.inf, args=(k, a), limit=50)[0]
    #
    # plt.plot(k_array, f_int)
    # plt.show()


k_min = 1
k_max = 100
k_array = np.linspace(k_min, k_max, 100)

#main(k_array=k_array, a=2.0/3.0)




def fun(f, kmin, kmax, knum=100, kscale="log", N=10000, h=0.01):
    """

    """

    H = hankel.HankelTransform(
        nu=1,
        N=N,
        h=h
    )

    if kscale == "log":
        k = np.logspace(
            np.log10(kmin),
            np.log10(kmax),
            knum
        )

    return (
        k,
        H.transform(
            f,
            k,
            ret_err=False
        )
    )

# k, H_k = fun(
#     f=lambda x : x**(-1.0 / 3.0),
#     kmin=10**-1.0,
#     kmax=10**2.0,
#     knum=100,
#     kscale="log"
# )
#
# plt.plot(k, H_k)
# plt.xscale("log")
# plt.yscale("log")
# plt.show()

ht = hankel.HankelTransform(
    nu= 0,     # The order of the bessel function
    N=10000,   # Number of steps in the integration
    h=0.01   # Proxy for "size" of steps in integration
)


# f = lambda x : np.exp(-x**2.0)
# H_f = lambda k : np.exp(-k**2.0 / 4.0) / 2.0

# f = lambda x : 1.0 / x
# H_f = lambda k : 1 / k

# f = lambda x : x**3.0
# H_f = lambda k : 9.0 / k**5.0

# f = lambda x : x
# H_f = lambda k : -1.0 / k**3.0

# f = lambda x : x
# H_f = lambda k : -1.0 / k**3.0

def power_law_HT(k, m):

    return 2.0**(m + 1) * special.gamma(m / 2.0 + 1.0) / (k**(m + 2.0) * special.gamma(-m / 2.0))

m = -1.0
f = lambda x : x**m
H_f = lambda k : power_law_HT(k=k, m=m)

k = np.logspace(-1,1,50)
Fk = ht.transform(f,k,ret_err=False)
plt.plot(k,Fk, color="black", label="numerical")


plt.plot(k,H_f(k), linewidth=4, color="b", alpha=0.5, label="analytical")

plt.legend()
plt.xscale('log')
#plt.yscale('log')
plt.ylabel(r"$H(k)$", fontsize=15)
plt.xlabel(r"$k$", fontsize=15)
plt.show()
