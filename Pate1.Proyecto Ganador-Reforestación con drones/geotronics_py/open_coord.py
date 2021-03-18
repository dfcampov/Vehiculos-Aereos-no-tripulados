with open("coord_1m.csv") as f:
    f.readline()
    for line in f:
        lista = line.split(",")
        longitude = lista[4]
        latitude= lista[5]
        