from math import log2
from sys import maxsize
class DecisionTree:
    def __init__(self, exemplos, atributos, classe):
        """
        :param exemplos: Exemplos do problema
        :type exemplos: list(list(str))
        :param atributos: Atributos do problema
        :type atributos: dict(str,int)
        :param classe: Classes
        :type classe: str
        """
        self.classe = classe
        self.possibleObjectives = []
        for i in range(len(exemplos)):
            try:
                self.possibleObjectives.index(exemplos[i][-1])
            except ValueError:
                self.possibleObjectives.append(exemplos[i][-1])

        self.root = None
        ''' Guardar atrinutos e o seu inverso'''
        self.atributosG_Str_Int = atributos
        self.atributosG_Int_Str = {v: k for k, v in atributos.items()}
        self.__madeTree(exemplos, atributos)


    def classify(self):
        pass

    def entropy(self, exemplos, atributo, flag=False):
        """
        :type atributo: int
        :return: int | (list(str),list(list(int)),list(list(int)))
        """
        diferAtr = []  # type: list(str)
        diferAtrExamp = [] # type: list(list(int))

        for i in range(len(exemplos)):
            try: #podria passar isto para dicionário
                aux = diferAtr.index(exemplos[i][atributo])
                diferAtrExamp[aux].append(i)
            except ValueError:
                diferAtr.append(exemplos[i][atributo])
                diferAtrExamp.append([i])

        if flag:
            classeRep = [[0 for _ in range(len(self.possibleObjectives))] for _ in range(len(diferAtr))]
            for i in range(len(diferAtrExamp)):
                for ex in diferAtrExamp[i]:
                    classeRep[i][self.possibleObjectives.index(exemplos[i][-1])] += 1
            return diferAtr, diferAtrExamp, classeRep

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
        """
        :type atributos: dict      
        :type exemplos: list(list(str))
        """

        decision = self.makeDecision(exemplos,atributos)  # type: str

        #del atributos[decision]

        self.root = self.__ID3(exemplos,decision,atributos)

    def makeDecision(self, exemplos, atributos):
        """
            :type atributos: dict      
            :type exemplos: list(list(str))
            :return: str
        """

        entropias = [None for _ in range(len(atributos) - 1)]  # é removido dois pq uma para atributo classe e outro ID

        for key, val in atributos.items():
            if key is not self.classe and key != 'ID':
                entropias[val] = self.entropy(exemplos, val)

        entropias[0] = maxsize
        print(list(zip(atributos.keys(), entropias)))

        decision = entropias.index(min(entropias))
        return self.atributosG_Int_Str[decision]

    def __ID3(self, examples, target_atribute, atributes):
        """
        :type examples: 
        :type target_atribute: str
        :type atributes: 
        :return: Node
        """
        del atributes[target_atribute]

        atrNames, atrExam, finalAns = self.entropy(examples, self.atributosG_Str_Int[target_atribute] , True)

        node = Node_root(target_atribute)

        incomplete = [] # lista de conjunto de dados aos quais não chegamos a nenhuma conclusão
        for i in range(atrNames):
            flag = True
            for x in finalAns[i]:
                if x != 0:
                    if flag:
                        classe = self.possibleObjectives[finalAns[i].index(x)]
                        flag = False
                    else:
                        incomplete.append(i)
                        flag = True
                        break

            if not flag:
                node.append(Leaf(atrNames[i], classe, len(atrExam[i])))

        if atributes:
            '''Caso ainda faltem atributos a ser processados'''
            for i in incomplete:
                aux_exam = [examples[x] for x in range(len(examples)) if x in atrExam[i]]
                decision = self.makeDecision(examples, atributes)
                no_aux = self.__ID3(aux_exam,decision,atributes)
                node.append(Jump(atrNames[i],no_aux,len(atrExam[i])))
        else:
            for i in incomplete:
                answer = atrNames[i]
                count = len(atrExam[i])
                label = self.possibleObjectives[finalAns[i].index(max(finalAns[i]))]
                node.append(Leaf(answer, label, count))

        return node


class Ramo:
     pass


class Leaf(Ramo):
    """
    :type answer: str
    :type label: str
    :type counter: int
    """

    def __init__(self, answer, label, counter):
        '''
        :param answer: Opção de resposta ao nó pai
        :type answer: str
        :param label: Classe respondida
        :type label: str
        :param counter: Numero de exemplos identificados
        :type counter: int
        '''
        self.answer = answer
        self.label = label
        self.counter = counter


class Jump(Ramo):
    """
        :type answer: str
        :type counter: int
        :type jump: Node_root
    """
    def __init__(self, answer, jump, counter):
        self.answer = answer
        self.jump = jump
        self.counter = counter


class Node_root:
    """
    :type atributo: str
    :type answers: list(Ramo)
    """
    def __init__(self,atributo):
        self.atributo = atributo
        self.answers = []

    def append(self,item):
        self.answers.append(item)