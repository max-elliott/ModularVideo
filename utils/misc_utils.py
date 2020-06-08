
def dataname_to_index(name):
    types = {
        'video': 0,
        'audio': 1,
        'modulation': 2
    }
    return types[name]
