
funcs  = [lambda x=x: x**2 for x in range(5)]

for i in range(5):
    print (funcs[i]())
