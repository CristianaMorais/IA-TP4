# /usr/bin/env python3
# -*- coding: utf-8 -*-

from math import log2
from sys import maxsize
from copy import deepcopy


class DecisionTree:
    minimoElem = 4

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
        self.transformations = {}
        self.possibleObjectives = []
        for i in range(len(exemplos)):
            try:
                self.possibleObjectives.index(exemplos[i][-1])
            except ValueError:
                self.possibleObjectives.append(exemplos[i][-1])

        ''' Guardar atrinutos e o seu inverso'''
        self.atributosG_Str_Int = atributos
        self.atributosG_Int_Str = {v: k for k, v in atributos.items()}

        '''Preparar examples'''
        for i in range(1, len(atributos)):
            try:
                float(exemplos[0][i])
                self.transform(exemplos, i)
            except ValueError:
                pass
        self.examples = deepcopy(exemplos)

        self.root = None

        self.__madeTree(exemplos, deepcopy(atributos))

        self.root.rearange()

    def classify(self, dict):
        '''
        :param dict: dicionário que pretendemos aporar a verdade
        :type dict: dict(str,str)
        :return: str
        '''
        for key, val in self.transformations.items():
            try:
                dict[key] = val[val.index(float(dict[key]))]
            except ValueError:
                return None

        return self.root.classify(dict)

    def entropy(self, exemplos, atributo, flag=False):
        """
        :type atributo: int
        :return: int | (list(str),list(list(int)),list(list(int)))
        """
        diferAtr = []  # type: list(str)
        diferAtrExamp = []  # type: list(list(int))

        for i in range(len(exemplos)):
            try:  # podria passar isto para dicionário
                aux = diferAtr.index(exemplos[i][atributo])
                diferAtrExamp[aux].append(i)
            except ValueError:
                diferAtr.append(exemplos[i][atributo])
                diferAtrExamp.append([i])

        if flag:
            for i in range(len(self.examples)):
                try:
                    diferAtr.index(self.examples[i][atributo])
                except ValueError:
                    diferAtr.append(self.examples[i][atributo])
                    diferAtrExamp.append([])

            classeRep = [[0 for _ in range(len(self.possibleObjectives))] for _ in range(len(diferAtr))]
            for i in range(len(diferAtrExamp)):
                for ex in diferAtrExamp[i]:
                    classeRep[i][self.possibleObjectives.index(exemplos[ex][-1])] += 1
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
                    aux += -(i / len(conjunto)) * log2(i / len(conjunto))
                except ValueError:
                    pass

            resposta += (len(conjunto) / len(exemplos)) * (aux)

        return resposta

    def __madeTree(self, exemplos, atributos):
        """
        :type atributos: dict      
        :type exemplos: list(list(str))
        """

        decision = self.makeDecision(exemplos, atributos)  # type: str

        # del atributos[decision]

        self.root = self.__ID3(exemplos, decision, atributos)

    def makeDecision(self, exemplos, atributos):
        """
            :type atributos: dict      
            :type exemplos: list(list(str))
            :return: str
        """

        entropias = [None for _ in
                     range(len(self.atributosG_Str_Int) - 1)]  # é removido dois pq uma para atributo classe e outro ID

        for key, val in atributos.items():
            if key is not self.classe and key != 'ID':
                entropias[val] = self.entropy(exemplos, val)

        entropias[0] = maxsize
        # print(list(zip(atributos.keys(), entropias)))
        entropias = [x if x is not None else maxsize for x in entropias]
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

        atrNames, atrExam, finalAns = self.entropy(examples, self.atributosG_Str_Int[target_atribute], True)

        node = Node_root(target_atribute)

        incomplete = []  # lista de conjunto de dados aos quais não chegamos a nenhuma conclusão
        for i in range(len(atrNames)):
            flag = True
            if atrExam[i] == []:
                incomplete.append(i)
                continue
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

        if len(atributes) > 2:
            '''Caso ainda faltem atributos a ser processados'''
            for i in incomplete:
                aux_exam = [examples[x] for x in range(len(examples)) if x in atrExam[i]]
                '''Caso fosse dar origem a atrinuto sem exemplos'''
                if aux_exam:
                    decision = self.makeDecision(aux_exam, atributes)
                    no_aux = self.__ID3(aux_exam, decision, deepcopy(atributes))
                    node.append(Jump(atrNames[i], no_aux, len(atrExam[i])))
                else:
                    '''caso não exista exemplos'''
                    node.append(Leaf(atrNames[i], self.mostCommon(), 0))


        else:
            for i in incomplete:
                answer = atrNames[i]
                count = len(atrExam[i])
                label = self.possibleObjectives[finalAns[i].index(max(finalAns[i]))]
                node.append(Leaf(answer, label, count))

        return node

    '''Trocar número para o geral'''

    def mostCommon(self):
        examples = self.examples
        classeRep = [0 for _ in range(len(self.possibleObjectives))]
        for aux in examples:
            classeRep[self.possibleObjectives.index(aux[-1])] += 1

        return self.possibleObjectives[classeRep.index(max(classeRep))]

    '''Efetua a transfromação dos exemplos'''

    def transform(self, exemplos, index):
        """
        :type exemplos: list(list(str))
        :type index: int
        :type atributos: dict(str,int) 
        """
        lista = [(float(exemplos[u][index]), exemplos[u][-1]) for u in range(len(exemplos))]

        lista.sort()

        aux = []

        encher_chouriços = False
        i = 0
        for num, target in lista:
            if i == 0:
                aval = target
                first = num
            elif i >= self.minimoElem:
                if aval != target or encher_chouriços:
                    aux.append(Intervalo(first, num))
                    first = num
                    aval = target
                    encher_chouriços = False
                    i = 0

            elif aval != target:
                encher_chouriços = True
            i += 1
        aux.append(Intervalo(first, num + 0.1))

        for u in range(len(exemplos)):
            exemplos[u][index] = aux[aux.index(float(exemplos[u][index]))]

        self.transformations[self.atributosG_Int_Str[index]] = aux

    def __str__(self):
        return self.root.myStr()


class Ramo:
    pass


class Leaf(Ramo):
    """
    :type answer: str
    :type label: str
    :type counter: int
    """

    def __init__(self, answer, label, counter):
        """
        :param answer: Opção de resposta ao nó pai
        :param label: Classe respondida
        :type label: str
        :param counter: Numero de exemplos identificados
        :type counter: int
        """
        self.answer = answer
        self.label = label
        self.counter = counter

    def __str__(self):
        return str(self.answer) + ': ' + str(self.label) + ' (' + str(self.counter) + ')\n'

    def myStr(self, prof):
        return '\t' * prof + str(self.answer) + ': ' + str(self.label) + ' (' + str(self.counter) + ')\n'

    def classify(self, dict):
        return self.label

    def rearange(self):
        pass


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

    def __str__(self):
        return str(self.answer) + ':\n' + str(self.jump)

    def myStr(self, prof):
        return '\t' * prof + str(self.answer) + ':\n' + self.jump.myStr(prof + 1)

    def classify(self, dict):
        return self.jump.classify(dict)

    def rearange(self):
        self.jump.rearange()


class Node_root:
    """
    :type atributo: str
    :type answers: list(Ramo)
    """

    def __init__(self, atributo):
        self.atributo = atributo
        self.answers = []

    def append(self, item):
        self.answers.append(item)

    def __str__(self):
        frase = '<' + self.atributo + '>\n'
        for x in self.answers:
            frase += str(x)

        return frase

    def myStr(self, prof=0):
        frase = '\t' * prof + '<' + self.atributo + '>\n'
        for x in self.answers:
            frase += x.myStr(prof + 1)

        return frase

    def classify(self, dict):
        user_answer = dict[self.atributo]
        for x in self.answers:
            if type(x.answer) is Intervalo:
                if x.answer.inner(user_answer):
                    return x.classify(dict)
                continue

            if x.answer == user_answer:
                return x.classify(dict)

    def rearange(self):
        if type(self.answers[0].answer) == Intervalo:
            answerAux1 = []  # type: list(list(int))

            ve = [(self.answers[i].answer,
                   (lambda x: self.answers[i].label if type(self.answers[i]) is Leaf else None)(i), i) for i in
                  range(len(self.answers))]  # type: list(Intervalo)
            ve.sort()

            i = -1
            last = None  # type last:str
            for _, classe, index in ve:
                if classe is None or last != classe:
                    answerAux1.append([index])
                    last = classe
                    i += 1
                    continue
                answerAux1[i].append(index)

            del ve

            answerTMP=[]

            for lista in answerAux1:
                if type(self.answers[lista[0]]) is Jump:
                    answerTMP.append(self.answers[lista[0]])
                    continue

                minimo = self.answers[lista[0]].answer.minimo
                maximo = self.answers[lista[0]].answer.maximo
                label = self.answers[lista[0]].label
                count = 0

                for i in lista:
                    count += self.answers[i].counter
                    maximo = max(maximo, self.answers[i].answer.maximo)

                answerTMP.append(Leaf(Intervalo(minimo, maximo), label, count))

            self.answers = answerTMP

        for x in self.answers:
            x.rearange()


class Intervalo:
    def __init__(self, minimo, maximo):
        """
        :param minimo: minimo do intervalo (inclusivo)
        :param maximo: máximo do intervalo (exclusivo)
        """
        self.minimo = minimo
        self.maximo = maximo

    def inner(self, other):
        if type(other) is not Intervalo:
            return False

        if self.minimo <= other.minimo and other.maximo <= self.maximo:
            return True
        else:
            return False

    def __eq__(self, other):
        if type(self) == type(other):
            if self.minimo == other.minimo and self.maximo == other.maximo:
                return True
            else:
                return False

        if self.minimo <= other < self.maximo:
            return True
        else:
            return False

    def __lt__(self, other):
        if type(self) == type(other):
            return self.maximo <= other.minimo

    def __str__(self):
        return str(self.minimo) + ' <= x < ' + str(self.maximo)
