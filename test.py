from functools import wraps

def test(*args,**kwargs):
    return 'args'

def lazy_init(class_name):
    print(class_name)


class Person:
    def __init__(self, name, age):
        pass

def add_decorated(class_name,function_name):
    setattr(Person,'Person',test(Person))

add_decorated(Person,test)
p = Person("Derp", 13)
print(p)