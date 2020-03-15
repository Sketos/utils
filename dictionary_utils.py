
# TODO: raise error when args not in dictionary
def get_output_from_nested_dictionary(dictionary, *args):
    if args and dictionary:
        element = args[0]
        if element:
            value = dictionary.get(element)
            if len(args) == 1:
                return value
            else:
                return get_output_from_nested_dictionary(value, *args[1:])


def testing_get_output_from_nested_dictionary():
    dictionary = {
        "model_1":{
            "parameters":[0.0, 0.1]
        },
        "model_2":{
            "parameters":[1.0, 0.0]}
    }
    output = get_output_from_nested_dictionary(
        dictionary, *["model_1", "parameters"]
    )
    print(output)

if __name__ == "__main__":



    testing_get_output_from_nested_dictionary()
