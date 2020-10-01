'''
Created on Sep 28, 2020
ISSUE 76 This code intended to allow manual entry of events and tasks.
@author: cseal
'''
class ManualEntry: 
    def __init__(self,firstName,lastName,date,location): 
        self.firstName = firstName 
        self.lastName = lastName 
        self.date = date 
        self.location = location
        
    def printEntry(self):
        print(self.firstName)
        print(self.lastName)
        print(self.date)
        print(self.location)
    
    def RecieveNewEntry(self):
        self.firstName = input("Please enter the first name of the child involved with the event")
        self.lastName = input("Please enter the last name of the child involved with the event")
        self.date = input("Please enter the date of the event")
        self.location = input("Please enter the location of the event")
manualEntryDefault = ManualEntry("John","Doe","99.99.9999","FAKE ADDRESS") 
manualEntryDefault.printEntry()
manualEntryDefault.RecieveNewEntry()
manualEntryDefault.printEntry()