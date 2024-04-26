import hashlib, json, sys

def hashMe(msg=""):
    
    if type(msg) != str:
        msg = json.dumps(msg,sort_keys=True)
        
    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()  #hexdigest converts the hash to a hexadecimal representation.