from math import log2
from sys import maxsize
class DecisionTree:
    def __init__(self, exemplos, atributos, classe):
        '''
        :param exemplos: Exemplos do problema
        :type exemplos: list(list(str))
        :param atributos: Atributos do problema
        :type atributos: dict(str,int)
        :param classe: Classes
        :type classe: str
        '''
        self.classe = classe
        self.possibleObjectives = []
        for i in range(len(exemplos)):
            try:
                self.possibleObjectives.index(exemplos[i][-1])
            except ValueError:
                self.possibleObjectives.append(exemplos[i][-1])

        self.root = None
        self.__madeTree(exemplos, atributos)


    def classify(self):
        pass

    def entropy(self, exemplos, atributo):
        '''
        :type atributo: int
        :return: int
        '''
        diferAtr = []  # type: list(str)
        diferAtrExamp = [] # type: list(list(int))

        for i in range(len(exemplos)):
            try: #podria passar isto para dicionário
                aux = diferAtr.index(exemplos[i][atributo])
                diferAtrExamp[aux].append(i)
            except ValueError:
                diferAtr.append(exemplos[i][atributo])
                diferAtrExamp.append([1])

        del diferAtr


        resposta = 0

        for conjunto in diferAtrExamp:
            classeRep = [0 for _ in range(len(self.possibleObjectives))]

            for i in conjunto:
                classeRep[self.possibleObjectives.index(exemplos[i][-1])] += 1

            aux = 0
            for i in classeRep:
                try:
                    '''Devido a possibilidade de existir 0 , não existe logaritmo de 0'''
                    aux += -(i/len(conjunto))*log2(i/len(conjunto))
                except ValueError:
                    pass

            resposta += (len(conjunto)/len(exemplos))*(aux)

        return resposta

    def __madeTree(self, exemplos, atributos):
        '''
        :type atributos: dict      
        :type exemplos: list(list(str))
        '''

        entropias = [None for _ in range(len(atributos)-1)]  # é removido dois pq uma para atributo classe e outro ID

        for key, val in atributos.items():
            if key is not self.classe and key != 'ID':
                entropias[val] = self.entropy(exemplos, val)

        entropias[0] = maxsize
        print(list(zip(atributos.keys(),entropias)))

        entropias.index(min(entropias))






class Node:
    def __init__(self, id=None):
        self.id = id
        self.value = None  # classe
        self.counter = None # numero de exemplos nessa classe
        self.atributos = []

    def append(self,atr):
        """
        :param atr: Atributo para acrescentar ao nó
        :type atr: Node
        """
        self.atributos.append(atr)
