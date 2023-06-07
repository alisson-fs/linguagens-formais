from finite_automata import FiniteAutomata


CONCAT = '.'
OR = '|'
CLOSURE = '*'
LEAF = None
EPSILON = '&'


class Node:
    def __init__(self, c1: 'Node', c2: 'Node', operation, symbol) -> None:
        self.__c1 = c1
        self.__c2 = c2
        self.__operation = operation
        self.__symbol = symbol
        self.__index = None

    def is_leaf(self) -> bool:
        return self.__c1 is None and self.__c2 is None


    def is_nullable(self) -> bool:
        if self.__symbol == EPSILON:
            return True
        elif self.is_leaf():
            return False
        elif self.__operation == CONCAT:
            return self.__c1.is_nullable() and self.__c2.is_nullable()
        elif self.__operation == OR:
            return self.__c1.is_nullable() or self.__c2.is_nullable()
        elif self.__operation == CLOSURE:
            return True


    def get_firstpos(self) -> set:
        if self.__symbol == EPSILON:
            return set()
        elif self.is_leaf():
            return set([self.__index])
        elif self.__operation == CONCAT:
            if self.__c1.is_nullable():
                return self.__c1.get_firstpos().union(self.__c2.get_firstpos())
            else:
                return self.__c1.get_firstpos()
        elif self.__operation == OR:
            return self.__c1.get_firstpos().union(self.__c2.get_firstpos())
        elif self.__operation == CLOSURE:
            return self.__c1.get_firstpos()


    def get_secondpos(self) -> set:
        if self.__symbol == EPSILON:
            return set()
        elif self.is_leaf():
            return set([self.__index])
        elif self.__operation == CONCAT:
            if self.__c2.is_nullable():
                return self.__c1.get_secondpos().union(self.__c2.get_secondpos())
            else:
                return self.__c2.get_secondpos()
        elif self.__operation == OR:
            return self.__c1.get_secondpos().union(self.__c2.get_secondpos())
        elif self.__operation == CLOSURE:
            return self.__c2.get_secondpos()


    def get_followpos(self, followpos: dict) -> dict:
        if self.is_leaf():
            return followpos
        if self.__operation == CLOSURE:
            for index in self.get_firstpos():
                followpos[index] = followpos[index].union(self.get_secondpos())
        elif self.__operation == CONCAT:
            for index in self.__c1.get_secondpos():
                followpos[index] = followpos[index].union(self.__c2.get_firstpos())
        followpos = self.__c1.get_followpos(followpos)
        followpos = self.__c2.get_followpos(followpos)
        return followpos


    def set_index(self, index: int) -> int:
        if not self.is_leaf() and self.__operation != CLOSURE:
            index = self.__c1.set_index(index)
            index = self.__c2.set_index(index)
        elif self.__operation == CLOSURE:
            index = self.__c1.set_index(index)
        else:
            self.__index = index
            index += 1
        return index


    def get_alphabet(self, alphabet = None) -> set:
        if alphabet is None:
            alphabet = set()
        if self.is_leaf():
            if self.__symbol != '#':
                alphabet.add(self.__symbol)
        else:
            alphabet = self.__c1.get_alphabet(alphabet)
            alphabet = self.__c2.get_alphabet(alphabet)
        return alphabet


    def get_correspondents_symbol(self, correspondents = None) -> dict:
        if correspondents is None:
            correspondents = dict()
        if self.is_leaf():
            correspondents[self.__index] = self.__symbol
        else:
            correspondents = self.__c1.get_correspondents_symbol(correspondents)
            correspondents = self.__c2.get_correspondents_symbol(correspondents)
        return correspondents


class RegularExpression:
    def __init__(self, expression: str) -> None:
        self.__expression = expression

        self.__root = self.expression_to_tree(self.__expression + '.#')
        max_index = self.__root.set_index(1)
        self.__indexes = [i for i in range(1, max_index)]
        self.__alphabet = list(self.__root.get_alphabet())
        self.__alphabet.sort()
        self.__index_to_symbol = self.__root.get_correspondents_symbol()


    @property
    def root(self):
        return self.__root
    

    @root.setter
    def root(self, root):
        self.__root = root


    @property
    def alphabet(self):
        return self.__alphabet


    @alphabet.setter
    def alphabet(self, alphabet):
        self.__alphabet = alphabet


    @property
    def index_to_symbol(self):
        return self.__index_to_symbol


    @index_to_symbol.setter
    def index_to_symbol(self, index_to_symbol):
        self.__index_to_symbol = index_to_symbol


    @property
    def indexes(self):
        return self.__indexes


    @indexes.setter
    def indexes(self, indexes):
        self.__indexes = indexes


    def display(self) -> None:
        print(self.__expression)


    def export(self, filename: str) -> None:
        text = '#RE\n#Expression\n' + \
            f'{self.__expression}'
        with open(filename, 'w') as file:
            file.write(text)


    def expression_to_tree(self, expression: str) -> Node:
        if len(expression) == 1:
            return Node(None, None, LEAF, expression)

        if expression[-1] == CLOSURE:
            left, operation, right = self.get_branches(expression[:-1])
            c2 = self.expression_to_tree(right)
            if left is None:
                # Fecho do restante da expressão.
                return Node(c2, c2, CLOSURE, None)
            else:
                c1 = self.expression_to_tree(left)

            closure = Node(c2, c2, CLOSURE, None)
            return Node(c1, closure, operation, None)
            
        else:
            left, operation, right = self.get_branches(expression)
            # Processando parênteses redudantes
            while left is None:
                left, operation, right = self.get_branches(right)

            c1 = self.expression_to_tree(left)
            c2 = self.expression_to_tree(right)
            return Node(c1, c2, operation, None)


    def get_branches(self, expression: str) -> Node:
        # Verifica se tem parênteses.
        if expression[-1] == ')':
            # Caso tenha parênteses, pega tudo dentro dele como ramo da direita, o resto como ramo da 
            # esquerda e também pega o simbolo que relaciona os dois ramos.
            stack_parentheses = ['(']
            index = -1
            while len(stack_parentheses) > 0:
                index -= 1
                if expression[index] == stack_parentheses[-1]:
                    stack_parentheses.pop()
                elif expression[index] == ')':
                    stack_parentheses.append('(')

            if len(expression) is - index:
                return None, None, expression[1:-1]
            else:
                return expression[:index-1], expression[index-1], expression[index+1: -1]

        else:
            # Caso não tenha parênteses, só pega o símbolo e retorna como o ramo da direita
            return expression[:-2], expression[-2], expression[-1]
