'''
Created on October 18, 2020
ISSUE 75 This code is intended to be used to create test accounts.
@author: cseal
'''

class RewardAlgorithm:
    def __init__(self,eventID):
        self.eventID = eventID
        self.completed = False
        self.message ="Test message(constructor)"   


    
    def respond(self):
        self.completed = True
        '''
        Prompt the child for a response and read in a response
        '''
        readInMessage = "Placeholder message"
        self.message = readInMessage
'''
The remaining code shows that the algorithm runs as expected
'''
JohnnysRewards = RewardAlgorithm(18)
#adds one point
JohnnysRewards.completedTask()
JohnnysRewards.recievedReward(10)
print(JohnnysRewards.getPoints()) 