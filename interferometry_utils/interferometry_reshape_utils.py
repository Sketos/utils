


def reshape(a, n_b):

    if len(a.shape) > 1:
        return a.reshape(
            (int(a.shape[0] / n_b), n_b, -1)
        )
    else:
        return a.reshape(
            (int(a.shape[0] / n_b), n_b)
        )

# return a.reshape(
#     (int(reduce(lambda x, y: x*y, a.shape[:-1])), a.shape[-1])
# )

if __name__ == "__main__":
    pass
