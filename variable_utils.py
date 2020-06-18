
def variable_name(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]


if __name__ == "__main__":

    var = 0.0
    name = variable_name(
        var,
        globals()
    )[0]
    print(name)
