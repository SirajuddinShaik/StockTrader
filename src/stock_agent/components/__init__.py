def stock_names():
    f= open("src\stock-agent\components\stock_names.txt")
    l=[]
    for i in f.readlines():
        l.append(i.split('(')[-1].replace(")",""))

    f = open("src\stock-agent\components\stock_names.txt","w")
    f.writelines(l)
    print(l)