from abc import abstractmethod, ABC

from src.Cite import Cite


class Parser(ABC):
    @abstractmethod
    def parse(self, row: []) -> Cite:
        pass


class ScholarParser(Parser):

    def parse(self, row: []) -> Cite:
        return Cite(row[1], row[2], row[3], row[4], row[5], row[11], row[0], row[6], row[10])


class ScopusParser(Parser):
    def parse(self, row: []) -> Cite:
        return Cite(row[0], row[2], row[3], row[17], row[4], row[12], 0, row[13], row[14])
