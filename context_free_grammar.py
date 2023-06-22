from tabulate import tabulate


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
            for j, non_terminal_production in enumerate(non_terminal_productions):
                production = non_terminal + ' -> ' + non_terminal_production
                if i == len(self.__productions) - 1 and j == len(non_terminal_production) - 1:
                    text += production
                else:
                    text += production + '\n'
            i += 1

        with open(filename, 'w') as file:
            file.write(text)
    

    def factor(self) -> bool:
        count_steps = 0
        while True:
            # Limitando número de passos para garatir que não ficará em loop.
            if count_steps > 15:
                print('ERRO: A fatoração entrou em loop.')
                return False

            for non_terminal in self.__non_terminals:
                self._solve_direct_non_determinism(non_terminal)

            num_non_terminals_with_non_determinism_cases = 0
            for non_terminal in self.__non_terminals:
                # Verifica se existe não determinismo indireto e, caso tenha, converte para determinismo direto e resolve.
                has_indirect_non_determinism = self._convert_indirect_to_direct_non_determinism(non_terminal)
                if has_indirect_non_determinism:
                    num_non_terminals_with_non_determinism_cases += 1

            count_steps += 1

            if num_non_terminals_with_non_determinism_cases == 0:
                break
        
        return True


    def _solve_direct_non_determinism(self, non_terminal) -> None:
        non_determinism_cases = self._get_direct_non_determinism_cases(self.__productions[non_terminal])
        if len(non_determinism_cases) > 0:
            for alpha, betas in non_determinism_cases.items():
                # Criando novo não terminal.
                i = 1
                while True:
                    new_non_terminal = non_terminal + i * "'"
                    if new_non_terminal not in self.__non_terminals:
                        break
                    i += 1
                self.__non_terminals.append(new_non_terminal)
                self.__productions[new_non_terminal] = []

                # Atualizando produções com o novo não terminal.
                for beta in betas:
                    self.__productions[non_terminal].remove(alpha + beta)

                    new_production = alpha + new_non_terminal
                    if new_production not in self.__productions[non_terminal]:
                        self.__productions[non_terminal].append(new_production)

                    if beta == '':
                        beta = '&'

                    if beta not in self.__productions[new_non_terminal]:
                        self.__productions[new_non_terminal].append(beta)


    def _convert_indirect_to_direct_non_determinism(self, non_terminal: str) -> bool:
        productions_updated = self.__productions[non_terminal]
        while True:
            has_updated = False
            new_productions = []
            # Loop para tranformar produções indiretas em diretas.
            for non_terminal_production in productions_updated:
                first_symbol, rest_production = self._get_first_symbol_in_production_and_rest(non_terminal_production)
                if first_symbol == None:
                    continue

                # Caso o primeiro simbolo seja um terminal.
                if first_symbol in self.__terminals + ['&'] and non_terminal_production not in new_productions:
                    new_productions.append(non_terminal_production)
                
                # Caso o primeiro simbolo seja um não terminal.
                elif first_symbol in self.__non_terminals:
                    has_updated = True
                    first_symbol_productions = self.__productions[first_symbol]
                    for first_symbol_production in first_symbol_productions:
                        if first_symbol_production == '&' and rest_production != '':
                            new_production = rest_production
                        else:
                            new_production = first_symbol_production + rest_production
                        if new_production not in new_productions:
                            new_productions.append(new_production)
            
            productions_updated = new_productions
            if not has_updated:
                break

        # Verifica se existem casos de não determinismo direto nas novas produções e se tiver atualiza as produções com as novas.
        non_determinism_cases = self._get_direct_non_determinism_cases(new_productions)
        if len(non_determinism_cases) > 0:
            self.__productions[non_terminal] = new_productions
            return True
        else:
            return False


    # Pega os casos de não determinismo direto.
    def _get_direct_non_determinism_cases(self, productions: list) -> dict:
        non_determinism_cases = {}

        for current_production in productions:
            first_symbol, _ = self._get_first_symbol_in_production_and_rest(current_production)
            if first_symbol == None or first_symbol not in self.__terminals:
                continue

            i = 0
            while i < len(current_production):
                if i == 0:
                    possible_alpha = current_production
                else:
                    possible_alpha = current_production[:-i]
                
                # Loop para verificar se o possivel alpha existe no inicio de alguma outra produção.
                for production in productions:
                    if current_production == production:
                        continue

                    # Caso exista.
                    if possible_alpha == production[:len(possible_alpha)]:
                        if possible_alpha not in non_determinism_cases.keys():
                            non_determinism_cases[possible_alpha] = []

                        rest_current_production = current_production[len(possible_alpha):]
                        rest_production = production[len(possible_alpha):]
                        if rest_current_production not in non_determinism_cases[possible_alpha]:
                            non_determinism_cases[possible_alpha].append(rest_current_production)
                        if rest_production not in non_determinism_cases[possible_alpha]:
                            non_determinism_cases[possible_alpha].append(rest_production)

                # Caso tenha encontrado um alpha, passa para a proxima produção.
                if possible_alpha in non_determinism_cases.keys():
                    break
                i += 1

        return non_determinism_cases


    # Separa o primeiro simbolo da produção e o resto dela.
    def _get_first_symbol_in_production_and_rest(self, production: str) -> tuple:
        first_symbol = ''
        for index_char, char in enumerate(production):
            first_symbol += char
            if (first_symbol in self.__non_terminals or 
                first_symbol in self.__terminals or 
                first_symbol == '&'):

                rest_production = production[index_char + 1:]
                if index_char < len(production) - 1:
                    if production[index_char + 1] != "'":
                        return first_symbol, rest_production
                else:
                    return first_symbol, rest_production
        return None, None


    def remove_left_recursion(self) -> None:
        for i in range(1, len(self.__non_terminals) + 1):
            Ai = self.__non_terminals[i - 1]
            for j in range(1, i):
                Aj = self.__non_terminals[j - 1]
                for Ai_production in self.__productions[Ai]:
                    first_symbol, alpha = self._get_first_symbol_in_production_and_rest(Ai_production)
                    
                    if first_symbol == Aj and alpha != '':
                        self.__productions[Ai].remove(Ai_production)
                        for Aj_production in self.__productions[Aj]:
                            new_production = Aj_production + alpha
                            if new_production not in self.__productions[Ai]:
                                self.__productions[Ai].append(new_production)
            
            self._remove_direct_left_recursion(Ai)


    def _remove_direct_left_recursion(self, non_terminal: str) -> None:
        new_productions = {}
        productions_with_recursion = []

        for non_terminal_production in self.__productions[non_terminal]:
            first_symbol, _ = self._get_first_symbol_in_production_and_rest(non_terminal_production)
            if first_symbol == non_terminal:
                productions_with_recursion.append(non_terminal_production)

        if productions_with_recursion:
            new_non_terminal = non_terminal + "'"
            self.__non_terminals.append(new_non_terminal)
            new_non_terminal_productions = ['&']
            updated_non_terminal_productions = []

            for non_terminal_production in self.__productions[non_terminal]:
                _, beta = self._get_first_symbol_in_production_and_rest(non_terminal_production)
                if non_terminal_production in productions_with_recursion:
                    new_non_terminal_productions.append(beta + new_non_terminal)
                else:
                    updated_non_terminal_productions.append(non_terminal_production + new_non_terminal)

            self.__productions[non_terminal] = updated_non_terminal_productions
            self.__productions[new_non_terminal] = new_non_terminal_productions

        else:
            new_productions[non_terminal] = self.__productions[non_terminal]


    def _convert_indirect_to_direct_recursion(self) -> None:
        new_productions = self.__productions.copy()
        verified_non_terminals = []
        for Ai in self.__non_terminals:
            for Aj in self.__non_terminals:
                if Ai != Aj and Aj not in verified_non_terminals:
                    for Aj_production in self.__productions[Aj].copy():
                        if Ai == Aj_production[:len(Ai)]:
                            new_productions[Aj].remove(Aj_production)

                            for Ai_production in self.__productions[Ai]:
                                new_productions[Aj].append(Ai_production + Aj_production[len(Ai):])
            verified_non_terminals.append(Ai)

        self.__productions = new_productions


    def get_firsts(self) -> dict:
        # Define os firsts para os terminais.
        firsts = {terminal: set((terminal,)) for terminal in self.__terminals + ['&']}

        # Define os firsts para os não terminais.
        for non_terminal in self.__non_terminals:
            firsts[non_terminal] = set()

        # Calcula os firsts até não existirem mais atualizações.
        while True:
            firsts_updated = False
            for non_terminal, non_terminal_productions in self.__productions.items():
                for non_terminal_production in non_terminal_productions:
                    first_symbol_in_production, production_rest = self._get_first_symbol_in_production_and_rest(non_terminal_production)

                    # Se o primeiro simbolo da produção do não terminal for um terminal, adiciona ele aos firsts do não terminal.
                    if first_symbol_in_production in self.__terminals:
                        updated_non_terminal_first = firsts[non_terminal].union(firsts[first_symbol_in_production])

                    # Se o primeiro simbolo da produção do não terminal for epsilon, adiciona ele aos firsts do não terminal.
                    elif first_symbol_in_production == '&':
                        updated_non_terminal_first = firsts[non_terminal].union(set('&'))

                    # Se o primeiro simbolo da produção do não terminal for um não terminal: 
                    elif first_symbol_in_production in self.__non_terminals:
                        # Adiciona os firsts do não terminal da produção nos firsts do não terminal.
                        first_symbol_in_production_firsts = firsts[first_symbol_in_production]
                        updated_non_terminal_first = firsts[non_terminal].union(first_symbol_in_production_firsts - set('&'))

                        # Se nos firsts do não terminal da produção existir epsilon, adiciona também os firsts do 
                        # proximo simbolo, caso exista.
                        while '&' in first_symbol_in_production_firsts:
                            # Se a produção terminal sem encontrar um terminal, adiciona epsilon nos firsts.
                            if production_rest == '':
                                updated_non_terminal_first.update(set('&'))
                                break

                            first_symbol_in_production, production_rest = self._get_first_symbol_in_production_and_rest(production_rest)
                            first_symbol_in_production_firsts = firsts[first_symbol_in_production]
                            updated_non_terminal_first.update(first_symbol_in_production_firsts - set('&'))

                    if updated_non_terminal_first != firsts[non_terminal]:
                        firsts_updated = True
                        firsts[non_terminal] = updated_non_terminal_first

            if not firsts_updated:
                break
        
        return firsts


    def get_follows(self, firsts: dict = None) -> dict:
        if not firsts:
            firsts = self.get_firsts()
        
        follows = {non_terminal: set() for non_terminal in self.__non_terminals}
        follows[self.__initial_symbol] = set('$')

        while True:
            follows_updated = False
            for non_terminal, non_terminal_productions in self.__productions.items():
                for non_terminal_production in non_terminal_productions:
                    production_split = self._production_split(non_terminal_production)
                    nullable_or_non_existent_beta = False
                    for index_symbol, symbol in enumerate(production_split):
                        if symbol in self.__non_terminals:
                            updated_non_terminal_follows = follows[symbol].copy()

                            beta = production_split[index_symbol + 1:]
                            if len(beta) > 0:
                                beta_firsts = self._beta_firsts(beta, firsts)
                                updated_non_terminal_follows.update(beta_firsts - set('&'))

                                if '&' in beta_firsts and non_terminal != symbol:
                                    nullable_or_non_existent_beta = True
                            elif non_terminal != symbol:
                                nullable_or_non_existent_beta = True

                            if nullable_or_non_existent_beta:
                                updated_non_terminal_follows.update(follows[non_terminal])

                            if updated_non_terminal_follows != follows[symbol]:
                                follows_updated = True
                                follows[symbol] = updated_non_terminal_follows

            if not follows_updated:
                break

        return follows


    def _production_split(self, production: str) -> list:
        production_symbols = []
        while True:
            first_symbol, rest = self._get_first_symbol_in_production_and_rest(production)
            production_symbols.append(first_symbol)
            production = rest
            if production == None:
                break
            if len(production) == 0:
                break
        return production_symbols


    def _beta_firsts(self, beta, firsts) -> set:
        beta_firsts = set()
        for index_symbol, symbol in enumerate(beta):
            if '&' not in firsts[symbol]:
                beta_firsts.update(firsts[symbol])
                break
            beta_firsts.update(firsts[symbol] - set('&'))
            if index_symbol == len(beta) - 1:
                beta_firsts.add('&')
        return beta_firsts


    def isLL1(self, firsts: dict = None, follows: dict = None) -> bool:
        if not firsts:
            firsts = self.get_firsts()
        if not follows:
            follows = self.get_follows(firsts)

        for non_terminal in self.__non_terminals:
            if len(firsts[non_terminal].intersection(follows[non_terminal])) > 0:
                return False
        return True
    

    def create_LL1_analysis_table(self, firsts: dict = None, follows: dict = None) -> dict:
        if not firsts:
            firsts = self.get_firsts()
        if not follows:
            follows = self.get_follows(firsts)
        
        analysis_table = {}
        for non_terminal in self.__non_terminals:
            analysis_table[non_terminal] = {}
            for terminal in self.__terminals + ['$']:
                analysis_table[non_terminal][terminal] = None

            for non_terminal_production in self.__productions[non_terminal]:
                first_symbol, _ = self._get_first_symbol_in_production_and_rest(non_terminal_production)

                if first_symbol != '&':
                    first_symbol_firsts = firsts[first_symbol]
                    for first_symbol_first in first_symbol_firsts:
                        analysis_table[non_terminal][first_symbol_first] = non_terminal_production
                else:
                    non_terminal_follows = follows[non_terminal]
                    for non_terminal_follow in non_terminal_follows:
                        analysis_table[non_terminal][non_terminal_follow] = non_terminal_production
        
        return analysis_table


    def show_LL1_analysis_table(self, table_dict: dict) -> None:
        production_equivalent_number = {}
        num_productions = 1
        for non_terminal, productions in self.__productions.items():
            for production in productions:
                production_equivalent_number[(non_terminal, production)] = num_productions
                num_productions += 1


        first_line = list(table_dict.values())[0]
        headers = [''] + list([terminal for terminal in first_line.keys()])
        table_data = []
        for non_terminal, productions in table_dict.items():
            row = [non_terminal]
            for production in productions.values():
                if production == None:
                    row.append('')
                else:
                    row.append(production_equivalent_number[(non_terminal, production)])
            table_data.append(row)

        table = tabulate(
            tabular_data=table_data, 
            headers=headers, 
            tablefmt="fancy_grid", 
            stralign="center"
        )

        for p, n in production_equivalent_number.items():
            print(str(n) + ': ' + str(p[0]) + ' -> ' + str(p[1]))
        print(table)


    # Reconhece a sentença.
    def recognize_sentence_ll1(self, sentence: str) -> bool:
        firsts = self.get_firsts()
        follows = self.get_follows(firsts)
        if not self.isLL1(firsts, follows):
            print('ERRO: A gramática não é LL1.')
            return False
        
        analysis_table = self.create_LL1_analysis_table(firsts, follows)

        sentence_split = self._production_split(sentence)
        if sentence_split == [None]:
            if sentence == '':
                sentence_split = []
            else:
                return False

        w = sentence_split + ['$']
        for symbol in w:
            if symbol not in self.__terminals + ['$']:
                return False
        a = w.pop(0)
        stack = [self.__initial_symbol, '$']
        X = stack.pop(0)
        while X != '$':
            if X == a:
                X = stack.pop(0)
                a = w.pop(0)
            elif X in self.__terminals:
                return False
            elif analysis_table[X][a] == None:
                return False
            elif analysis_table[X][a] == '&':
                X = stack.pop(0)
            else:
                stack = self._production_split(analysis_table[X][a]) + stack
                X = stack.pop(0)

        return True
