

class Wallet:
    def __init__(self):
        """
        Attributes:
            - balances (dict): A dictionary storing the balances of different cryptocurrencies.
                               The keys are the cryptocurrency symbols (e.g., BTC, ETH), and
                               the values are the corresponding quantities held in the wallet.
                               Example: {'BTC': 0.5, 'ETH': 2.3, 'LTC': 5.1}
        """
        self.balances = {}

    def add_balance(self, symbol, quantity):
        if symbol in self.balances:
            self.balances[symbol] += quantity
        else:
            self.balances[symbol] = quantity
    
    def get_balance(self, symbol):
        return self.balances.get(symbol, 0)
    
    def remove_balance(self, symbol, quantity):
        if symbol in self.balances:
            if self.balances[symbol] >= quantity:
                self.balances[symbol] -= quantity
            else:
                raise ValueError("Insufficient balance")