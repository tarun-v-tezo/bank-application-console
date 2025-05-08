from datetime import datetime
from common.constants import Constants
from data.managers.bankManager import BankManager
from models.Bank import Bank
from models.NewBankRequest import NewBankRequest
from models.NewCurrencyRequest import NewCurrencyRequest
from models.UpdateChargeRequest import UpdateChargeRequest
from services.CurrencyService import CurrencyService


class BankService:
    currentBank: Bank = None
    def __init__(self):
        self.currencyService = CurrencyService()
        self.banks = BankManager.getBanks()

    @classmethod
    def setCurrentBankById(cls, bankId: str):
        bankService = cls()
        bank = bankService.getBankById(bankId)
        if bank is None:
            print(f"Bank with Id {bankId} not found.")
            return
        cls.currentBank = bank

    @classmethod
    def setCurrentBankByName(cls, bankName: str):
        bank = cls.getBankByName(bankName)
        if bank is None:
            print(f"Bank with Name {bankName} not found.")
            return
        cls.currentBank = bank
    
    @classmethod
    def setCurrentBank(cls, bank: Bank):
        cls.currentBank = bank
    
    def getBankById(self, bankId: str):
        for bank in self.banks:
            if bank.id == bankId:
                return bank
        return None

    def getBankByName(self, bankName: str):
        for bank in self.banks:
            if bank.name == bankName:
                return bank
        return None
    
    def addExistingAcceptedCurrencyToBank(self, bankId: str, currencyCode: str):
        newCurrency = self.currencyService.getAcceptedCurrencyByCode(currencyCode)
        if newCurrency is None:
            print(f"Currency with code {currencyCode} not found.")
            return None
        bank = self.getBankById(bankId)
        if bank is None:
            print(f"Bank with Id {bankId} not found.")
            return
        if newCurrency.id in bank.acceptedCurrencyIds:
            print(f"Currency {currencyCode} already accepted by bank {bank.name}.")
            return
        bank.acceptedCurrencyIds.append(newCurrency.id)
        BankManager.setBanks(self.banks)
        return bank.acceptedCurrencyIds
    
    def addNewAcceptedCurrencyToBank(self, bankId: str, newCurrency: NewCurrencyRequest):
        bank = self.getBankById(bankId)
        if bank is None:
            print(f"Bank with Id {bankId} not found.")
            return
        newAcceptedCurrency = self.currencyService.addAcceptedCurrency(newCurrency)
        if newAcceptedCurrency is None:
            print("Failed to add new accepted currency.")
            return
        bank.acceptedCurrencyIds.append(newAcceptedCurrency.id)
        BankManager.setBanks(self.banks)
        return bank.acceptedCurrencyIds
    
    def isCurrencyAcceptedByBank(self, bankId: str, currencyCode: str):
        bank = self.getBankById(bankId)
        if bank is None:
            print(f"Bank with Id {bankId} not found.")
            return False
        currency = self.currencyService.getAcceptedCurrencyByCode(currencyCode)
        if currency is None:
            print(f"Currency with code {currencyCode} not found.")
            return False
        if currency.id in bank.acceptedCurrencyIds:
            return True
        return False
    
    def updateServiceCharges(self, updateChargeRequest: UpdateChargeRequest):
        bank = self.getBankById(updateChargeRequest.bankId)
        if bank is None:
            print(f"Bank with Id {updateChargeRequest.bankId} not found.")
            return
        if updateChargeRequest.rtgs is not None:
            bank.rtgs = updateChargeRequest.rtgs
        if updateChargeRequest.imps is not None:
            bank.imps = updateChargeRequest.imps
        if updateChargeRequest.ortgs is not None:
            bank.ortgs = updateChargeRequest.ortgs
        if updateChargeRequest.oimps is not None:
            bank.oimps = updateChargeRequest.oimps
        
        BankManager.setBanks(self.banks)
        return bank
    
    def addBank(self, bank: NewBankRequest):
        if self.getBankByName(bank.name) is not None:
            print(f"Bank with name {bank.name} already exists.")
            return None
        newBank = Bank(
            id=f"{bank.name[:3]}{datetime.now().strftime('%Y%m%d')}",  # need to implement a better way to get the id
            name=bank.name,
            acceptedCurrencyIds= self.__addDefaultCurrencyToList(bank.acceptedCurrencyIds if bank.acceptedCurrencyIds else []),
            rtgs=bank.rtgs if bank.rtgs else Constants.DefaultRTGS,
            imps=bank.imps if bank.imps else Constants.DefaultIMPS,
            ortgs=bank.ortgs if bank.ortgs else Constants.DefaultORTGS,
            oimps=bank.oimps if bank.oimps else Constants.DefaultOIMPS
        )
        self.banks.append(newBank)
        BankManager.setBanks(self.banks)

        return bank
    
    def removeBank(self, bankName: str):
        for i,bank in enumerate(self.banks):
            if bank.name == bankName:
                self.banks.pop(i)
                BankManager.setBanks(self.banks)
                return True
        return False
    
    def __addDefaultCurrencyToList(self, acceptedCurrencyIds: list[str]):
        defaultCurrency = self.currencyService.getAcceptedCurrencyByCode(Constants.DefaultCurrencyCode)
        if defaultCurrency is None:
            print("Default currency not found.")
            return
        acceptedCurrencyIds.append(defaultCurrency.id)
        # Remove duplicates
        acceptedCurrencyIds = list(set(acceptedCurrencyIds))
        return acceptedCurrencyIds