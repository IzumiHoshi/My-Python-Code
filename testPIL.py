import hashlib

db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}

def cal_md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return(md5.hexdigest())

def login(username, password):
    if db.get(username) == cal_md5(password):
        return True
    else:
        return False

print(db.get('bob'))
print(login('bobs', 'abc999'))