import numpy as np
import matplotlib.pyplot as plt

def gaussian_process(sigma, n):

    a = np.zeros(shape=(n, ))

    for i in range(n-1):
        a[i+1] = np.random.normal(loc=a[i], scale=sigma)

    return a


if __name__ == "__main__":

    a = gaussian_process(sigma=0.01, n=1000)

    plt.plot(a)
    plt.show()
