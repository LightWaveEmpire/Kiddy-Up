'''
Created on October 1, 2020
This code intended to allow manual entry of events and tasks.
@author: cseal
'''
class ChildrenInformation: 
    def __init__(self,firstName,lastName,youngerGroup): 
        self.firstName = firstName 
        self.lastName = lastName 
        self.youngerGroup = True
        
    def createListOfChildren(self, numberOfChildren):
        i=0
        list = []
        while i<numberOfChildren:
            temp = input("What is the first name of child number" +i)
            temp2= input("What is the last name of child number" + i)
            temp3= input("What is the age of child number" + i)
            list.append(ChildrenInformation(temp,temp2,temp3))
            i =i +1
        return list