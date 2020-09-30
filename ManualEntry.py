'''
Created on Sep 28, 2020
This code intended to allow manual entry of events and tasks.
@author: cseal
'''
class ManualEntry: 
    
    
    def __init__(self, firstName, lastName,date,location): 
        self.firstName = firstName 
        self.lastName = lastName 
        self.date = date 
        self.location = location
        
    manualEntryDefault = ManualEntry("John","Doe","99.99.9999","FAKE ADDRESS") 
    
    
        
        