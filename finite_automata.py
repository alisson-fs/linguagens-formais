from tabulate import tabulate


class FiniteAutomata:

    def __init__(
            self,
            states: list,
            alphabet: list,
            transitions: dict,
            initial_state: str,
            accept_states: list
    ) -> None:
        self.__states = states
        self.__alphabet = alphabet
        self.__transitions = transitions
        self.__initial_state = initial_state
        self.__accept_states = accept_states


    @property
    def states(self):
        return self.__states


    @states.setter
    def states(self, states):
        self.__states = states


    @property
    def alphabet(self):
        return self.__alphabet


    @alphabet.setter
    def alphabet(self, alphabet):
        self.__alphabet = alphabet
    

    @property
    def transitions(self):
        return self.__transitions


    @transitions.setter
    def transitions(self, transitions):
        self.__transitions = transitions


    @property
    def initial_state(self):
        return self.__initial_state


    @initial_state.setter
    def initial_state(self, initial_state):
        self.__initial_state = initial_state


    @property
    def accept_states(self):
        return self.__accept_states


    @accept_states.setter
    def accept_states(self, accept_states):
        self.__accept_states = accept_states
            

    # Determinização.
    def NFA_to_DFA(self, clean_automata: bool = False) -> None:
        transitions = self.__transitions
        # Calcula e-fecho e verifica se tem transições por epsilon.
        epsilon_closure, has_epsilon_closure = self._calculate_epsilon_closure()

        # Caso o calculo do e-fecho tenha alterado o estado inicial, atualiza ele.
        if epsilon_closure[self.__initial_state] != self.__initial_state:
            self.__initial_state = epsilon_closure[self.__initial_state]
            self._check_accept_state(self.__initial_state)

        # Se houver transições por epsilon, limpa as transições e coloca apenas o estado inicial.
        # Caso contratio, anula as transições de todos os estados para recalcula-las.
        if has_epsilon_closure:
            self.__states = [self.__initial_state]
            self.__transitions = {self.__initial_state: [None] * len(self.__alphabet)}
        else:
            self.__transitions = {}
            for state in self.__states:
                self.__transitions[state] = [None] * len(self.__alphabet)

        # Define as novas transições.
        self._define_new_transitions(epsilon_closure, transitions)

        if clean_automata:
            self._clean_automata()


    def _calculate_epsilon_closure(self) -> tuple:
        # Inicializa o e-fecho com os estados iniciais.
        epsilon_closure = self._initialize_epsilon_closure()
        for state in self.__states:
            states = []
            alphabet_size = len(self.__alphabet)
            # Se houver um IndexError, quer dizer que não existem transições por epsilon.
            # Caso contrario, atualiza o e-fecho do estado.
            try:
                transition = self.__transitions[state][alphabet_size]
            except IndexError:
                return (epsilon_closure, False)
            else:
                states.append(state)
                if (transition != '-'):
                    transition = transition.split(',')
                    states.extend(transition)
                    states = list(set(map(str, states)))
                    states.sort()
                    epsilon_closure[state] = ','.join(states)
        return epsilon_closure, True


    # Inicializa e-fecho.
    def _initialize_epsilon_closure(self) -> dict:
        epsilon_closure = {}
        for state in self.__states:
            epsilon_closure[state] = state
        return epsilon_closure


    # Verifica se a transição possui estados de aceitação e, caso tenha, adiciona.
    def _check_accept_state(self, transition: list) -> None:
        states = transition.split(',')
        for state in states:
            if state in self.__accept_states and transition not in self.__accept_states:
                self.__accept_states.append(transition)


    # Retira os estados de aceitação que não estão mais em estados.
    def _clean_accept_states(self) -> None:
        for accept_state in self.__accept_states:
            if accept_state not in self.__states:
                self.__accept_states.remove(accept_state)


    # Define as novas transições do automato determinizado.
    def _define_new_transitions(self, epsilon_closure: dict, transitions: dict) -> None:
        for state in self.__states:
            for i in range(len(self.__alphabet)):
                if self.__transitions[state][i] == None:
                    # Pega todos os estados que esse estado pode ter.
                    states_list = state.split(',')

                    # Pega todas as transições do estado.
                    state_to_transit_list = []
                    for item_states_list in states_list:
                        state_to_transit_list.append(transitions[item_states_list][i])
    
                    # Adiciona as transições por epsilon dos estados na nova transição.
                    state_to_transit = []
                    for state_transit in state_to_transit_list:
                        if (state_transit != '-'):
                            if (len(state_transit.split(',')) > 1):
                                state_transit = state_transit.split(',')
                                for s in state_transit:
                                    state_to_transit.extend(epsilon_closure[s].split(','))
                            else:
                                state_to_transit.extend(epsilon_closure[state_transit].split(','))
    
                    state_to_transit = list(set(state_to_transit))
                    state_to_transit.sort()
                    state_to_transit = ','.join(map(str, state_to_transit))

                    # Se o novo estado gerado não estiver na lista dos estados, adiciona.
                    if state_to_transit and state_to_transit not in self.__states:
                        self.__states.append(state_to_transit)
                        self.__transitions[state_to_transit] = [None] * len(self.__alphabet)
                        # Verifica se o novo estado deve fazer parte dos estados de aceitação.
                        self._check_accept_state(state_to_transit)
    
                    # Se o estado não houver transição, define ela como '-'.
                    if not state_to_transit:
                        state_to_transit = '-'
    
                    # Atualiza a transição.
                    self.__transitions[state][i] = state_to_transit
        # Retira os estados de aceitação que não fazem mais parte dos estados.
        self._clean_accept_states()


    # Printa o automato em formato de tabela no terminal.
    def display(self) -> None:
        table_data = []
        states = [s for s in self.__transitions.keys()]
        transitions = [t for t in self.__transitions.values()]
        for i in range(len(states)):
            state = states[i]
            prefix = ''
            if state == self.__initial_state:
                prefix += '->'
            if state in self.__accept_states:
                prefix += '*'
            state = prefix + state

            line = []
            line.append(state)
            for transition in transitions[i]:
                line.append(transition)
            table_data.append(line)

        headers = [a for a in self.__alphabet]
        _, has_epsilon_closure = self._calculate_epsilon_closure()
        if has_epsilon_closure:
            headers.append('&')
        headers.insert(0, '')
        
        table = tabulate(
            tabular_data=table_data, 
            headers=headers, 
            tablefmt="fancy_grid", 
            stralign="center"
        )
        print(table)


    # Exporta o automato em um arquivo válido como entrada.
    def export(self, filename: str):
        text = f'#FA\n#States\n' + \
            f'{" | ".join(self.__states)}\n' + \
            f'#InitialState\n{self.__initial_state}\n' + \
            '#AcceptStates\n' +\
            f'{" | ".join(self.__accept_states)}\n' +\
            '#Alphabet\n' +\
            f'{" | ".join(self.__alphabet)}\n' + \
            '#Transitions\n'

        transitions = list(self.__transitions.values())
        for i in range(len(self.__states)):
            state = self.__states[i]
            transition = transitions[i]
            if i == len(self.__states)-1:
                text += state + ' -> ' + ' | '.join(transition)
            else:
                text += state + ' -> ' + ' | '.join(transition) + '\n'
        with open(filename, 'w') as file:
            file.write(text)


    # Minimização.
    def minimize(self, clean_automata: bool = False) -> None:
        if clean_automata:
            self._clean_automata()
        # Determiniza.
        self.NFA_to_DFA(clean_automata=True)
        # Remove estados inalcançáveis.
        self._remove_unreachable_states()
        # Remove estados mortos.
        self._remove_dead_states()
        # Junta estados equivalentes com algoritmo de partições de Hopcroft.
        self._unite_equivalent_states()


    def _remove_unreachable_states(self) -> None:
        # Inicia a lista de estados alcançaveis pelo estado inicial.
        reachable_states_list = [self.__initial_state]
        # Percorre a lista de estados alcançaveis adicionando os estados que são alcançaveis pelas transições.
        for state in reachable_states_list:
            new_reachable_states = []
            transitions = self.__transitions[state]
            for transition_state in transitions:
                if ((transition_state not in reachable_states_list) and 
                    (transition_state not in new_reachable_states) and 
                    (transition_state != '-')):
                    new_reachable_states.append(transition_state)
            reachable_states_list.extend(new_reachable_states)

        self.__states = list(set(self.__states).intersection(reachable_states_list))
        self.__accept_states = list(set(self.__accept_states).intersection(reachable_states_list))
        self.__transitions = {s: t for s, t in self.__transitions.items() if s in self.__states}


    def _remove_dead_states(self) -> None:
        # Inicia a lista de estados vivos pelos estados de aceitação.
        alive_states = []
        alive_states.extend(self.__accept_states)
        # Percorre a lista de estados adicionando a lista de estados vivos os estados que tem transição para estados vivos.
        while True:
            new_alive = False
            for state in self.__states:
                new_alive_states = []
                transitions = self.__transitions[state]
                for transition_state in transitions:
                    if ((transition_state in alive_states) and 
                        (state not in alive_states) and 
                        (state not in new_alive_states) and 
                        (transition_state != '-')):
                        new_alive = True
                        new_alive_states.append(state)
                alive_states.extend(new_alive_states)
            if not new_alive:
                break

        self.__states = list(set(self.__states).intersection(alive_states))
        self.__transitions = {s: t for s, t in self.__transitions.items() if s in alive_states}
        self.__transitions = {s: [t if t in alive_states else '-' for t in ts] for s, ts in self.__transitions.items()}


    def _unite_equivalent_states(self) -> None:
        F = self.__accept_states
        K_minus_F = list(set(self.__states) - set(self.__accept_states))
        #  Define partições iniciais com estados finais e não finais.
        P = [F, K_minus_F]
        # Loop que roda até as partições pararem de se dividirem.
        while True:
            has_division = False
            # Para cada partição, procura se há algum estado não equivalente.
            for partition in P:
                found_non_equivalent_states = self._has_non_equivalent_states(P, partition)
                has_division = has_division or found_non_equivalent_states
                # Caso encontre estados não equivalentes, começa a busca novamente pelas partições.
                if found_non_equivalent_states:
                    break
            # Caso não tenha ocorrido nenhuma dividão de estado de equivalencia, 
            # atualiza as transições do automato com os novos estados.
            if not has_division:
                self._update_transitions(P)
                break

    
    def _update_transitions(self, P) -> None:
        # Atualiza o estado inicial.
        initial_equivalent_state_index = self._search_for_partition_index(self.__initial_state, P)
        self.__initial_state = 'q' + str(initial_equivalent_state_index)

        # Cria os novos estados.
        new_states = ['q' + str(i) for i in range(0, len(P))]
        new_transitions = {state: [] for state in new_states}
        new_accept_states = []

        # Loop para gerar as transições entre os novos estados e definir os novos estados de aceitação.
        for i in range (0, len(P)):
            equivalent_state = new_states[i]
            # Pega um estado da partição.
            state = P[i][0]
            # Verifica se esse estado da partição e de aceitação e adiciona o estado de equivalencia 
            # deste estado nos novos estados de aceitação.
            if state in self.__accept_states:
                new_accept_states.append(equivalent_state)

            # Define as transições dos novos estados do automato.
            for symbol in range(0, len(self.__alphabet)):
                transition = self.__transitions[state][symbol]
                target_partition_index = self._search_for_partition_index(transition, P)
                if target_partition_index == -1:
                    new_transitions[equivalent_state].append('-')
                else:
                    transicao_equivalent_state = 'q' + str(target_partition_index)
                    new_transitions[equivalent_state].append(transicao_equivalent_state)

        self.__states = new_states
        self.__transitions = new_transitions
        self.__accept_states = new_accept_states


    def _has_non_equivalent_states(self, P, partition) -> bool:
        # Faz o mapeamento de transições de cada estado da partição para a partição com estado destino.
        mapping = {}
        for symbol in range(0,len(self.__alphabet)):
            for index in range(-1, len(P)):
                mapping[index] = []

            # Procura a partição que contém o estado destino e pega seu índice.
            for state in partition:
                target_state = self.__transitions[state][symbol]
                target_partition_index = self._search_for_partition_index(target_state, P)
                mapping[target_partition_index].append(state)
            # Caso existam estados não equivalentes, separa a partição.
            if self._non_equivalents_states_exist(mapping):
                new_partition = self._convert_mapping_to_partition(mapping)
                P.extend(new_partition)
                P.remove(partition)
                return True

        return False


    # Retorna o indice da particao onde se encontra o estado destino.
    def _search_for_partition_index(self, target_state, P) -> int:
        for index in range(0, len(P)):
            for state_partition in P[index]:
                if state_partition == target_state:
                    return index
        return -1


    # Verifica se existem estados que não são equivalentes.
    def _non_equivalents_states_exist(self, mapping) -> bool:
        division_count = 0
        for index in mapping:
            if len(mapping[index]) > 0:
                division_count += 1
        return division_count > 1

    # Converte o mapeamento de uma particao para uma nova particao.
    def _convert_mapping_to_partition(self, mapping) -> list:
        partition = []
        for index in mapping:
            if len(mapping[index]) > 0:
                partition.append(mapping[index])
        return partition

    # Renomeia os estados do automato para que os estados com subestados fiquem mais legíveis.
    def _clean_automata(self) -> None:
        new_initial_state = 'q0'
        new_states = ['q' + str(i) for i in range(0, len(self.__states))]
        new_transitions = {state: [] for state in new_states}
        new_accept_states = []
        self._clean_transitions(new_states, new_transitions, new_accept_states)
        _, has_epsilon_closure = self._calculate_epsilon_closure()
        if has_epsilon_closure:
            self._clean_epsilon_transitions(new_states, new_transitions)
        self.__states = new_states
        self.__transitions = new_transitions
        self.__initial_state = new_initial_state
        self.__accept_states = new_accept_states


    # Atualiza transições por simbolos do alfabeto com os estados do automato correspondente aos 
    # estados do automato original sem considerar subestados.
    def _clean_transitions(
            self, 
            new_states: list, 
            new_transitions: dict, 
            new_accept_states: list,
            base_index: int = 0
    ) -> None:
        j = base_index
        for state in self.__states:
            correspondent_state = new_states[j]
            for i in range(0, len(self.__alphabet)):
                state_transition = self.__transitions[state][i]
                if state_transition == '-':
                    new_transitions[correspondent_state].append('-')
                    continue
                new_transition_index = self.__states.index(state_transition)
                new_transitions[correspondent_state].append(new_states[new_transition_index])
                if state in self.__accept_states:
                    new_accept_states.append(correspondent_state)
            j += 1


    # Atualiza transições por epsilon com os estados do automato correspondente aos estados do 
    # automato original sem considerar subestados..
    def _clean_epsilon_transitions(
            self,
            new_states: list,
            new_transitions: dict,
            base_index: int = 0
    ) -> None:
        i = len(self.__alphabet)
        j = base_index
        for state in self.__states:
            correspondent_state = new_states[j]
            j += 1
            try:
                state_transition = self.__transitions[state][i]
            except IndexError:
                new_transitions[correspondent_state].append('-')
            else:
                if state_transition == '-':
                    new_transitions[correspondent_state].append('-')
                    continue
                new_transition_index = self.__states.index(state_transition)
                new_transitions[correspondent_state].append(new_states[new_transition_index])


    # Atualiza transições por simbolos do alfabeto com os estados do automato correspondente aos estados do automato original.
    def update_new_transitions(
            self, 
            new_transitions: dict, 
            new_states: list, 
            base_index: int, 
            new_accept_states: list 
    ) -> None:
        j = base_index
        for state in self.__states:
            correspondent_state = new_states[j]
            for i in range(0, len(self.__alphabet)):
                transition = self.__transitions[state][i]
                if transition == '-':
                    new_transitions[correspondent_state].append('-')
                    continue
                new_transition = []
                for state_transition in transition.split(','):
                    original_state_index = self.__states.index(state_transition)
                    new_transition.append(new_states[original_state_index + base_index])
                new_transition = ','.join(map(str, new_transition))
                new_transitions[correspondent_state].append(new_transition)
                if state in self.__accept_states:
                    new_accept_states.append(correspondent_state)
            j += 1


    # Atualiza transições por epsilon com os estados do automato correspondente aos estados do automato original.
    def update_new_epsilon_transitions(
            self,
            new_transitions: dict,
            new_states: list,
            base_index: int
    ) -> None:
        i = len(self.__alphabet)
        j = base_index
        for state in self.__states:
            correspondent_state = new_states[j]
            j += 1
            try:
                transition = self.__transitions[state][i]
            except IndexError:
                new_transitions[correspondent_state].append('-')
            else:
                if transition == '-':
                    new_transitions[correspondent_state].append('-')
                    continue
                new_transition = []
                for state_transition in transition.split(','):
                    original_state_index = self.__states.index(state_transition)
                    new_transition.append(new_states[original_state_index + base_index])
                new_transition = ','.join(map(str, new_transition))
                new_transitions[correspondent_state].append(new_transition)


    # Reconhece a sentença.
    def recognize_sentence(self, sentence: str) -> bool:
        self._clean_automata()
        # Determiniza o automato.
        self.NFA_to_DFA()
        # Verifica se todos os simbolos da sentença estão no alfabeto.
        if not all([symbol in self.__alphabet for symbol in sentence]):
            return False
        # Percorre o automato com a sentença de entrada.
        current_state = self.__initial_state
        for symbol in sentence:
            symbol_index = self.__alphabet.index(symbol)
            current_state = self.__transitions[current_state][symbol_index]
        # Verifica se o último estado é estado de aceitação.
        return current_state in self.__accept_states
