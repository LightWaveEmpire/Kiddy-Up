'''
Created on October 18, 2020
ISSUE 75 This code is intended to be used to create test accounts.
@author: cseal
'''
from test.pydoc_mod import __xyz__
class Rewards
    def __init__(self,currentPoints):
        self.currentPoints = currentPoints
    '''
    This will have to be modified to reflect being read in from the database
    '''
    def completedTask(self):
        self.currentPoints =self.currentPoints + 1
        return self.currentPoints
    
    def getPoints(self):
        return self.currentPoints
    '''
    This will have to be modified to reflect being read in from the database
    '''
    def RecievedReward(self,valueOfReward):
        self.currentPoints = self.currentPoints - valueOfReward

        