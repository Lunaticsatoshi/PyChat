from jinja2 import Undefined

def _slice(iterable, pattern):
    """
    Custom Slicing method to use 
    inside Jinja Templates
    :param pattern: string ex (::-1)
    :param iterable: string
    :return string
    """
    if iterable is None or isinstance(iterable, Undefined):
        return iterable

    #converting to list
    items = str(iterable)

    start = None
    end = None
    stride = None

    #Split the pattern 
    if pattern:
        tokens = pattern.split(':')
        print(tokens)
        if len(tokens) > 1:
            start = int(tokens[0])
        if len(tokens) > 2:
            end = int(tokens[1])
        if len(tokens) > 3:
            stride = int(tokens[2])
    
    return items[start:end:stride]