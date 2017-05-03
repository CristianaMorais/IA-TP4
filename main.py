import csv
from decisiontree import DecisionTree

def main():
    ficheiro = 'restaurant.csv'

    '''Leitura do ficheiro CSV'''
    with open(ficheiro,'rt') as fd:

        exemplosBuf= csv.reader(fd)
        firstRow = exemplosBuf.__next__()

        exemplos=[]  # type: list(list(str))
        for i in exemplosBuf:
            exemplos.append(i)

        atributos = {}  # type: dict(str,int)

        for i in range(len(firstRow)):
            atributos[firstRow[i]] = i

        classe = firstRow[-1]
        fd.close()

    arvore = DecisionTree(exemplos, atributos, classe)






if __name__ == '__main__':
    main()