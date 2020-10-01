'''
Created on October 1, 2020
ISSUE 75 This code is intended to be used to create test accounts.
@author: cseal
'''
import ManualEntry
import ChildrenInformation

class CreateAccount:
    def __init__(self,accountCreator,numberOfChildren,):
        self.accountCreator= accountCreator
        self.list = CreateListofChildren(numberOfChildren)