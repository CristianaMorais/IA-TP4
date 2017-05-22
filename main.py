import csv
from decisiontree import DecisionTree
from argparse import ArgumentParser
from sys import argv, exit


def main():
    parser = ArgumentParser(description='Porcessador de dados utilizando ID3.')

    parser.add_argument('-e','--examples', type=str, help='Documento com os dados que queremeos que a máquina aprenda.')
    parser.add_argument('-p', '--print', action='store_true', help='Imprimir a árvore.')
    parser.add_argument('-t', '--testes', type=str, help='Documentos onde se encontram os dados que se prentende avaliar.')

    args = parser.parse_args()

    if len(argv) == 1:
        parser.print_help()
        exit(0)

    '''Leitura do ficheiro CSV dos exemplos'''
    with open(args.examples ,'rt') as fd:

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

    if args.print:
        print(arvore)

    if args.testes is not None:
        '''Leitura do csv dos testes'''
        with open(args.testes, 'rt') as fd:
            exemplosBuf = csv.reader(fd)
            firstRow = exemplosBuf.__next__()

            for aux in exemplosBuf:
                dicio = {}  # type: dict(str,str)
                for i in range(len(firstRow)):
                    dicio[firstRow[i]] = aux[i]

                '''Procurar resposta'''
                print(arvore.classify(dicio))

                del dicio

            fd.close()


if __name__ == '__main__':
    main()