import pickle

ERROR_NONE = 0b0
ERROR_PHYSICAL = 0b1
ERROR_EMULATOR = 0b10
ERROR_BOTH = 0b11

MODE = ("arm", "thumb", "arm64")


def parse_pickled_file(path):
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data


def pickle_file(path, obj):
    with open(path, "wb") as f:
        pickle.dump(obj, f)
