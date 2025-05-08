from models.AcceptedCurrency import AcceptedCurrency
from ..database import Database
from common.constants import DataKeys


class AcceptedCurrencyManager:
    __acceptedCurrencies = []

    @classmethod
    def initialize(cls):
        cls.__acceptedCurrencies = [AcceptedCurrency(**currencyData) for currencyData in Database.getData(DataKeys.ACCEPTEDCURRENCIES)]

    @classmethod
    def getAcceptedCurrencies(cls):
        return cls.__acceptedCurrencies.copy()

    @classmethod
    def setAcceptedCurrencies(cls, acceptedCurrencies):
        cls.__acceptedCurrencies = acceptedCurrencies
        Database.setData(DataKeys.ACCEPTEDCURRENCIES, cls.__acceptedCurrencies)