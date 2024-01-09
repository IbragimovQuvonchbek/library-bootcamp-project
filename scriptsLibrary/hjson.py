from json import load, dump, JSONDecodeError


def read_data(file):
    try:
        with open(file) as f:
            data = load(f)
        return data
    except (FileNotFoundError, JSONDecodeError):
        with open(file, 'w') as f:
            dump([], f)
        return []


def write_data(file, data):
    with open(file, 'w') as f:
        dump(data, f, indent=4)
