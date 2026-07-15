from abc import (
    ABC,
    abstractmethod
)


class ComposingRule(ABC):
    @abstractmethod
    def matches(self, left, right):
        pass

    @abstractmethod
    def apply(self, left, right):
        pass