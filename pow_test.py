from hashlib import sha256
import datetime

print('------start------')
start = datetime.datetime.now()
a = 0
while True:
    b = sha256(str(a).encode()).hexdigest()[-6:]
    if b == '000000':
        break
    a = a + 1

print(sha256(str(a).encode()).hexdigest())
print(a)
end = datetime.datetime.now()
print((end - start).seconds)
