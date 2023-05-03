from abc import ABC, abstractmethod


class FinanceBotAbstract(ABC):
    """ """

    def __init__(self) -> None:
        self.pair = ''

    @abstractmethod
    def buy(self) -> None:
        ...

    @abstractmethod
    def sell(self) -> None:
        ...

    def should_buy(self) -> bool:
        ...

    def should_sell(self) -> bool:
        ...

    def main_loop(self) -> None:
        """ should fetch data
        process data
        check buy / sell condition
        log
        log + chart at the end
        """
        ...

    def chart(self):
        ...

    def log_wallet(self):
        ...

    def log_gain(self):
        ...

    def __str__(self) -> str:
        """ special methods called by print """
        return "test"
    

Ft = FinanceBotAbstract()
print(Ft)
