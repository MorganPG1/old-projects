import test
for name, item in test.getSystemInfo().items():
    print(name+":",item)
for name, item in test.getKernelInfo().items():
    print(name+":",item)
for name, item in test.getNetworkInfo().items():
    print(name+":",item)