
def singleton(cls, *args, **kw):
    instances = {}
    def getinstance():
        print('----------------------------------------------------------------')
        print(instances)
        print('----------------------------------------------------------------')
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance