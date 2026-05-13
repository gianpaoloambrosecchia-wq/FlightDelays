from dataclasses import dataclass

from model.airport import Airport


@dataclass
class Tratta:
    aeroportoP: Airport
    aeroportoD: Airport
    peso: int

    def __hash__(self):
        return hash((self.aeroportoP, self.aeroportoD))

    def __eq__(self, other):
        return self.aeroportoP == other.aeroportoP and other.aeroportoD == other.aeroportoD