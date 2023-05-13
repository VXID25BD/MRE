import logging
import os
from typing import List, Union


class FileManager:
    """
    Managing files
    """
    @staticmethod
    def get_files() -> List[str]:
        """
        Get all filenames in current category with extension .txt
        :return: all filenames in current category with extension .txt
        """
        return [file for file in os.listdir(os.getcwd()) if os.path.isfile(file) and file.endswith('.txt') and not file.startswith("requirements.txt")]

    @staticmethod
    def overwrite_lines(strings: Union[List[str], set[str]], path: str) -> None:
        """
        Overwriting lines in file
        :param strings: lines on overwriting
        :param path: path to file
        :return:
        """
        with open(path, "w", encoding="utf-8") as file:
            for string in strings:
                file.write(string + "\n")

    @staticmethod
    def read_lines(path: str) -> List[str]:
        """
        Reading lines from file
        :param path: path to file
        :return: lines
        """
        with open(path, "r") as file:
            return file.read().splitlines()
