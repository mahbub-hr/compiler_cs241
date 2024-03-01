class res:
    def __init__(self, x):
        self.x = x
        
def foo(ob):
    ob = dic[0]
    ob.x = 1
    return ob


dic = {}
dic[0] = res(0)
print(dic[0].x)
re = foo(None)
print(dic[0].x)