import hashlib, json, sys, random
random.seed(0)

def hashMe(msg=""):
    
    if type(msg) != str:
        msg = json.dumps(msg,sort_keys=True)
        
    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()  #hexdigest converts the hash to a hexadecimal representation.


def makeTransaction(maxValue=3):
    
    sign = int(random.getrandbits(1))*2 -1 
    amount = random.randint(1,maxValue)
    user1Pays = sign * amount
    user2Pays = -1 * user1Pays
    
    
    return {u'user One':user1Pays, u'User Two':user2Pays}

txnBuffer = [makeTransaction() for i in range(30)]

def updateState(txn,state):
    
    state = state.copy()
    
    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state