import os
import numpy as np
import multiprocessing



if __name__ == "__main__":



    """
    def print_arg(arg):
        print(arg)

    def print_ID():
        print(
            "The process ID is {}".format(
                os.getpid()
            )
        )

    print(os.getpid())

    p1 = multiprocessing.Process(target=print_ID)
    p2 = multiprocessing.Process(target=print_ID)

    p1.start()
    p2.start()

    print(p1.pid)
    print(p2.pid)

    p1.join()
    p2.join()

    print(p1.is_alive())
    """


    def function(args):

        uv_wavelengths, n = args

        return uv_wavelengths * n


    uv_wavelengths = np.random.normal(0.0, 1.0, size=(128, 1000))

    arglist = [
        [uv_wavelengths[n, :], n] for n in range(uv_wavelengths.shape[0])
    ]

    #mylist = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,44,554,334,23,23,4,343,432,43]

    # creating a pool object
    p = multiprocessing.Pool()

    # map list to target function
    result = p.map(function, arglist)

    #print(np.shape(result))
    print(result[0][:])




# # import multiprocessing as mp
# # print("Number of processors: ", mp.cpu_count())
#
# # from multiprocessing import Process
# # import os
# #
# # def info(title):
# #     print(title)
# #     print('module name:', __name__)
# #     if hasattr(os, 'getppid'):  # only available on Unix
# #         print('parent process:', os.getppid())
# #     print('process id:', os.getpid())
# #
# # def f(name):
# #     info('function f')
# #     print('hello', name)
# #
# # if __name__ == '__main__':
# #     info('main line')
# #     p = Process(target=f, args=('bob',))
# #     p.start()
# #     p.join()
#
# import numpy as np
#
# # Prepare data
# np.random.RandomState(100)
# arr = np.random.randint(0, 10, size=[200000, 5])
# data = arr.tolist()
# data[:5]
#
# def howmany_within_range(row, minimum, maximum):
#     """Returns how many numbers lie within `maximum` and `minimum` in a given `row`"""
#     count = 0
#     for n in row:
#         if minimum <= n <= maximum:
#             count = count + 1
#     return count
#
# import multiprocessing as mp
#
# # Step 1: Init multiprocessing.Pool()
# pool = mp.Pool(mp.cpu_count())
#
# # Step 2: `pool.apply` the `howmany_within_range()`
# results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]
#
# # Step 3: Don't forget to close
# pool.close()
#
# print(results[:10])
# #> [3, 1, 4, 4, 4, 2, 1, 1, 3, 3]
