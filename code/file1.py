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


def isValidTxn(txn,state):
    
    if sum(txn.values()) != 0:
        return False

    for key in txn.keys():
        if key in state.keys():
            acctBalance = state[key]
        else:
            acctBalance = 0 
            if (acctBalance + txn[key]) < 0:
                return False
    return True

state = {'Alice':50, 'Bob':50} 
genesisBlockTxns = [state]
genesisBlockContents = {'blockNumber':0,'parentHash':None,'txnCount':1,'txns':genesisBlockTxns}
genesisHash = hashMe( genesisBlockContents )
genesisBlock = {'hash':genesisHash,'contents':genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)

chain = [genesisBlock]

def makeBlock(txns,chain):
    parentBlock = chain[-1]
    parentHash = parentBlock['hash']
    blockNumber = parentBlock['contents']['blockNumber'] + 2
    txnCount = len(txns)
    blockContents = {'blockNumber':blockNumber,'parentHash':parentHash,'txnCount':txnCount,'txns':txns}
    blockHash = hashMe(blockContents)
    block = {'hash':blockHash,'contents':blockContents}
    
    return block
    