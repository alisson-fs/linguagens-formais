class RegularGrammar:
    def __init__(
            self, 
            non_terminals: list, 
            terminals: list, 
            productions: list, 
            initial_symbol: str
    ) -> None:
        self.__non_terminals = non_terminals
        self.__terminals = terminals
        self.__productions = productions
        self.__initial_symbol = initial_symbol
    

    @property
    def non_terminals(self) -> list:
        return self.__non_terminals


    @non_terminals.setter
    def non_terminals(self, non_terminals) -> None:
        self.__non_terminals = non_terminals


    @property
    def terminals(self) -> list:
        return self.__terminals


    @terminals.setter
    def terminals(self, terminals) -> None:
        self.__terminals = terminals

    @property
    def productions(self) -> list:
        return self.__productions


    @productions.setter
    def productions(self, productions) -> None:
        self.__productions = productions


    @property
    def initial_symbol(self) -> str:
        return self.__initial_symbol


    @initial_symbol.setter
    def initial_symbol(self, initial_symbol) -> None:
        self.__initial_symbol = initial_symbol


    def display(self):
        grammar_productions = {}
        for production in self.__productions:
            production_split = production.split(' -> ')
            if production_split[0] in grammar_productions.keys():
                grammar_productions[production_split[0]].append(production_split[1])
            else:
                grammar_productions[production_split[0]] = [production_split[1]]

        for non_terminal, productions in grammar_productions.items():
            productions_str = ' | '.join(productions)
            print(f'{non_terminal} -> {productions_str}')


    def export(self, filename):
        text = '#RG\n' + \
            '#NonTerminals\n' + \
            f'{" | ".join(self.__non_terminals)}\n' + \
            '#Terminals\n' + \
            f'{" | ".join(self.__terminals)}\n' + \
            '#InitialSymbol\n' + \
            f'{self.__initial_symbol}\n' + \
            '#Productions\n'
        for i in range(len(self.__productions)):
            production = self.__productions[i]
            if i == len(self.__productions)-1:
                text += production
            else:
                text += production + '\n'

        with open(filename, 'w') as file:
            file.write(text)


    def separate_production(self, production) -> tuple:
        production_split = production.split(' -> ')
        current_non_terminal = production_split[0]
        terminal = None
        for t in self.__terminals:
            if t in production_split[1]:
                terminal = t
                break

        non_terminal = None
        for nt in self.__non_terminals:
            if nt in production_split[1]:
                non_terminal = nt
                break

        has_epsilon = False
        if '&' in production_split[1]:
            has_epsilon = True

        return current_non_terminal, terminal, non_terminal, has_epsilon
