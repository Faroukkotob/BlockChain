from file1 import updateState, isValidTxn, makeTransaction, hashMe

state = {'Alice':5,'Bob':5}

print(isValidTxn({'Alice': -3, 'Bob': 3},state)) 
print(isValidTxn({'Alice': -4, 'Bob': 3},state))  
print(isValidTxn({'Alice': -6, 'Bob': 6},state))  
print(isValidTxn({'Alice': -4, 'Bob': 2,'Lisa':2},state)) 
print(isValidTxn({'Alice': -4, 'Bob': 3,'Lisa':2},state))