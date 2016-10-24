import json

d= dict(name = 'Bob', age = '20', scroe ='88')

print(json.dumps(d))


import pickle

print(pickle.dumps(d))

