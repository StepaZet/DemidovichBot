class FileManager:
    def __init__(self, file_names: list[str], mode: str = 'rb'):
        self.__file_names = file_names
        self.__files = []
        self.mode = mode

    def __enter__(self) -> list:
        self.__files = [
            open(file_name, self.mode) for file_name in self.__file_names
        ]
        return self.__files

    def __exit__(self, exc_type, exc_val, exc_tb):
        for file in self.__files:
            file.close()
