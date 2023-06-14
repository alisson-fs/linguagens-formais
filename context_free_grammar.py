class ContextFreeGrammar:
    def __init__(
            self, 
            non_terminals: list, 
            terminals: list, 
            productions: dict, 
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
    def productions(self) -> dict:
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
        for non_terminal, non_terminal_productions in self.__productions.items():
            non_terminal_productions_str = ' | '.join(non_terminal_productions)
            print(f'{non_terminal} -> {non_terminal_productions_str}')


    def export(self, filename: str):
        text = '#CFG\n' + \
            '#NonTerminals\n' + \
            f'{" | ".join(self.__non_terminals)}\n' + \
            '#Terminals\n' + \
            f'{" | ".join(self.__terminals)}\n' + \
            '#InitialSymbol\n' + \
            f'{self.__initial_symbol}\n' + \
            '#Productions\n'
        i = 0
        for non_terminal, non_terminal_productions in self.__productions.items():
            for non_terminal_production in non_terminal_productions:
                production = non_terminal + ' -> ' + non_terminal_production
                if i == len(self.__productions)-1:
                    text += production
                else:
                    text += production + '\n'
            i += 1

        with open(filename, 'w') as file:
            file.write(text)


    def factor(self) -> None:
        num_new_non_terminals = 0

        # Não determinismo direto.
        for non_terminal in self.__non_terminals:
            num_new_non_terminals = self._solve_direct_non_determinism(non_terminal, num_new_non_terminals)
        
        # Não deterministo indireto.
        count_steps = 0
        for non_terminal in self.__non_terminals:
            # Limitando número de passos para garatir que não ficará em loop.
            if count_steps > 15:
                print('ERRO: Alcançou o limite de passos.')
                break

            # Verifica se existe não determinismo indireto e, caso tenha, converte para determinismo direto e resolve.
            has_indirect_non_determinism = self._convert_indirect_to_direct_non_determinism(non_terminal)
            if has_indirect_non_determinism:
                num_new_non_terminals = self._solve_direct_non_determinism(non_terminal, num_new_non_terminals)
                count_steps += 1


    def _solve_direct_non_determinism(self, non_terminal, num_new_non_terminals) -> int:
        non_determinism_cases = self._get_direct_non_determinism_cases(self.__productions[non_terminal])
        if len(non_determinism_cases) > 0:
            for terminal, rest_productions in non_determinism_cases.items():
                # Criando novo não terminal.
                new_non_terminal = 'J' + str(num_new_non_terminals)
                num_new_non_terminals += 1
                self.__non_terminals.append(new_non_terminal)
                self.__productions[new_non_terminal] = []

                # Atualizando produções com o novo não terminal.
                for rest_production in rest_productions:
                    if rest_production == '':
                        rest_production = '&'

                    self.__productions[non_terminal].remove(terminal + rest_production)

                    new_production = terminal + new_non_terminal
                    if new_production not in self.__productions[non_terminal]:
                        self.__productions[non_terminal].append(new_production)

                    if rest_production not in self.__productions[new_non_terminal]:
                        self.__productions[new_non_terminal].append(rest_production)

        return num_new_non_terminals


    def _convert_indirect_to_direct_non_determinism(self, non_terminal: str) -> bool:
        new_productions = []
        productions_to_remove = []
        # Loop para tranformar produções indiretas em diretas.
        for non_terminal_production in self.__productions[non_terminal]:
            first_symbol, rest_production = self._get_first_symbol_in_production_and_rest(non_terminal_production)
            if first_symbol == None:
                continue

            # Caso o primeiro simbolo seja um terminal.
            if first_symbol in self.__terminals and non_terminal_production not in new_productions:
                new_productions.append(non_terminal_production)
            
            # Caso o primeiro simbolo seja um não terminal.
            elif first_symbol in self.__non_terminals:
                first_symbol_productions = self.__productions[first_symbol]
                for first_symbol_production in first_symbol_productions:
                    new_production = first_symbol_production + rest_production
                    if new_production not in new_productions:
                        new_productions.append(new_production)
                    if non_terminal_production not in productions_to_remove:
                        productions_to_remove.append(non_terminal_production)

        # Verifica se existem casos de não determinismo direto nas novas produções e se tiver atualiza as produções com as novas.
        non_determinism_cases = self._get_direct_non_determinism_cases(new_productions)
        if len(non_determinism_cases) > 0:
            for production_to_remove in productions_to_remove:
                self.__productions[non_terminal].remove(production_to_remove)
            for new_production in new_productions:
                self.__productions[non_terminal].append(new_production)
            return True
        else:
            return False


    # Pega os casos de não determinismo direto.
    def _get_direct_non_determinism_cases(self, non_terminal_productions: list) -> dict:
        # Dicionario que contém os terminais e as produções no qual ele faz parte.
        productions_with_terminal_on_left_side = {}
        for non_terminal_production in non_terminal_productions:
            first_symbol, rest_production = self._get_first_symbol_in_production_and_rest(non_terminal_production)
            if first_symbol == None:
                continue
            if first_symbol in self.__terminals:
                if first_symbol not in productions_with_terminal_on_left_side.keys():
                    productions_with_terminal_on_left_side[first_symbol] = []
                productions_with_terminal_on_left_side[first_symbol].append(rest_production)
        
        non_determinism_cases = {}
        for terminal, rest_productions_with_terminal in productions_with_terminal_on_left_side.items():
            if len(rest_productions_with_terminal) > 1:
                non_determinism_cases[terminal] = rest_productions_with_terminal
        
        return non_determinism_cases


    # Separa o primeiro simbolo da produção e o resto dela.
    def _get_first_symbol_in_production_and_rest(self, production: str) -> tuple:
        first_symbol = ''
        for char in production:
            first_symbol += char
            if first_symbol in self.__non_terminals or first_symbol in self.__terminals:
                rest_production = production.replace(first_symbol, '')
                return first_symbol, rest_production
        return None, None
