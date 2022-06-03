import abc


class Step(abc.ABC):
    def __init__(self, instruction):
        self.instruction = instruction

    @abc.abstractmethod
    def verify(self, hands):
        pass
