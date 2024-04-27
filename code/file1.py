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

    sign = int(random.getrandbits(1))*2 - 1  
    amount = random.randint(1,maxValue)
    alicePays = sign * amount
    bobPays   = -1 * alicePays
    return {u'Alice':alicePays,u'Bob':bobPays}


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

state = {u'Alice':50, u'Bob':50}  # Define the initial state
genesisBlockTxns = [state]
genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}
genesisHash = hashMe( genesisBlockContents )
genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)

chain = [genesisBlock]

def makeBlock(txns,chain):
    parentBlock = chain[-1]
    parentHash  = parentBlock[u'hash']
    blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
    txnCount    = len(txns)
    blockContents = {u'blockNumber':blockNumber,u'parentHash':parentHash,
                     u'txnCount':len(txns),'txns':txns}
    blockHash = hashMe( blockContents )
    block = {u'hash':blockHash,u'contents':blockContents}
    
    return block

blockSizeLimit = 5  

while len(txnBuffer) > 0:
    bufferStartSize = len(txnBuffer)
    
    txnList = []
    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        validTxn = isValidTxn(newTxn,state)
        
        if validTxn:         
            txnList.append(newTxn)
            state = updateState(newTxn,state)
        else:
            print("ignored transaction")
            sys.stdout.flush()
            continue  
        
    myBlock = makeBlock(txnList,chain)
    chain.append(myBlock) 
    
print(chain[0])
print(chain[1])
print("STATE: ",state)