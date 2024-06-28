class distances:
    file = open('distances.csv','r')
    for line in file:
        line = line.strip()
        field = line.split(',')
        print(field)



