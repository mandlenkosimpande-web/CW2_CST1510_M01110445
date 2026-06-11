import bcrypt



#hashed by using bycrpt
def generates_hash(psw):
    bytes_psw = psw.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes_psw, salt)
    return hashed.decode('utf-8')

#validating hash vs password
def is_valid_hash(psw, hash):
    hash_ = hash.encode('utf-8')
    byte_psw = psw.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash_)
    return is_valid

#user registration


#user login 


