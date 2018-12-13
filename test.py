# import jwt
#
# key = 'secret'
# encoded = jwt.encode({'some': 'payload'}, key, algorithm='HS256')
# print(encoded)
#
# header, payload, signature = encoded.split(b'.')
# print(header)
# print(payload)
# print(signature)
# print('*'*30)
#
#
# # 1、获取算法对象
# from jwt.algorithms import get_default_algorithms
# import base64
# import json
#
# alg = get_default_algorithms()['HS256']
# new_key = alg.prepare_key(key)  # key为secret
#
# # 2、获取前两部分 header.payload
# signing_input, _, _ = encoded.rpartition(b'.')
# print(signing_input)
#
# # 3、使用key签名
# signature = alg.sign(signing_input, new_key)
# print('+'*30)
# print(signature)
# print(base64.urlsafe_b64encode(signature))
# print(base64.urlsafe_b64encode(json.dumps({'payload': 'abc123'}).encode()))

# def add_eq(x: bytes):
#     rest = 4 - len(x) % 4
#     return x + b'=' * rest
#
#
# import base64
# print(base64.urlsafe_b64decode(add_eq(header)))
# print(base64.urlsafe_b64decode(add_eq(payload)))
# print(base64.urlsafe_b64decode(add_eq(signature)))
#
# print('-'*30)
# payload = jwt.decode(encoded, 'secret', algorithms=['HS256'])
# print(payload)
# # {'some': 'payload'}


import jwt
import datetime
from blog.settings import SECRET_KEY
import threading

payload = {
    'test': 'abc',
    'exp': int(datetime.datetime.now().timestamp() + 5)
}

encoded = jwt.encode(payload, SECRET_KEY)
print(encoded)
print(1, jwt.get_unverified_header(encoded))
event = threading.Event()

while not event.wait(1):
    try:
        pl = jwt.decode(encoded, SECRET_KEY, algorithms=['HS256'])
        print(pl)
    except jwt.ExpiredSignatureError as e:
        print(e, '----------------')
        break

print(2, jwt.get_unverified_header(encoded))








