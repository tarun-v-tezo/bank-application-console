import json


class Database:
    __file_path = 'C:/Codes/Python/Bank Task/data/data.json'
    __data = {}

    @classmethod
    def initialize(cls):
        cls.__data = cls.__loadData()

    @classmethod
    def __loadData(cls):
        try:
            with open(cls.__file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error loading data.")
            return {}

    @classmethod
    def getData(cls, key: str):
        return cls.__data.get(key, [])

    @classmethod
    def setData(cls, key: str, value):
        cls.__data[key] = [item.__dict__ for item in value]
        cls.__saveData()

    @classmethod
    def __saveData(cls):
        with open(cls.__file_path, 'w') as file:
            json.dump(cls.__data, file, indent=4)