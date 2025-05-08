from data.managers.acceptedCurrencyManager import AcceptedCurrencyManager
from models.AcceptedCurrency import AcceptedCurrency
from models.NewCurrencyRequest import NewCurrencyRequest


class CurrencyService:
    def __init__(self):
        self.acceptedCurrencies = AcceptedCurrencyManager.getAcceptedCurrencies()

    def getAcceptedCurrencyByCode(self, currencyCode):
        for currency in self.acceptedCurrencies:
            if currency.currencyCode == currencyCode:
                return currency
        return None
    
    def getCurrencyIdByCode(self, currencyCode):
        for currency in self.acceptedCurrencies:
            if currency.currencyCode == currencyCode:
                return currency.id
        return None
    
    def getAcceptedCurrencyById(self, currencyId):
        for currency in self.acceptedCurrencies:
            if currency.id == currencyId:
                return currency
        return None

    def addAcceptedCurrency(self, newCurrency: NewCurrencyRequest):
        if self.getAcceptedCurrencyByCode(newCurrency.currencyCode) is not None:
            print(f"Currency with code {newCurrency.currencyCode} already exists.")
            return None
        newAcceptedCurrency = AcceptedCurrency(
            id=len(self.acceptedCurrencies) + 1,  # need to implement a better way to get the id
            currencyCode=newCurrency.currencyCode,
            currencyName=newCurrency.currencyName,
            symbol=newCurrency.symbol,
            exchangeRate=newCurrency.exchangeRate,
        )
        self.acceptedCurrencies.append(newAcceptedCurrency)
        AcceptedCurrencyManager.setAcceptedCurrencies(self.acceptedCurrencies)
        return newAcceptedCurrency
    
    def convertCurrency(self, amount: float, fromCurrencyId: str, toCurrencyId: str) -> float:
        fromCurrency = self.getAcceptedCurrencyById(fromCurrencyId)
        toCurrency = self.getAcceptedCurrencyById(toCurrencyId)
        if fromCurrency is None or toCurrency is None:
            print("Invalid currency IDs.")
            return amount
        convertedAmount = amount * (toCurrency.exchangeRate / fromCurrency.exchangeRate)
        return convertedAmount