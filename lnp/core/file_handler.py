import json


class FileHandler:
    def __init__(self, file_path):
        self.__path = file_path

    def read(self) -> dict[str]:
        data = None
        with open(self.__path, "r") as fd:
            data = json.load(fd)
        return data
