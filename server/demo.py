import time
print(time.localtime(time.time()))
for i in range(8):
    print(time.localtime(time.time())[i])