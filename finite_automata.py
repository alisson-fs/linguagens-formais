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


    def NFA_to_FA(self) -> None:
        transitions = self.__transitions
        # Calcula e-fecho e verifica se tem transições por epsilon.
        epsilon_closure, has_epsilon_closure = self.calculate_epsilon_closure()

        # Caso o calculo do e-fecho tenha alterado o estado inicial, atualiza ele.
        if epsilon_closure[self.__initial_state] != self.__initial_state:
            self.__initial_state = epsilon_closure[self.__initial_state]
            self.check_accept_state(self.__initial_state)

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
        self.define_new_transitions(epsilon_closure, transitions)


    def calculate_epsilon_closure(self) -> tuple[dict, bool]:
        # Inicializa o e-fecho com os estados iniciais.
        epsilon_closure = self.initialize_epsilon_closure()
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
        return (epsilon_closure, True)


    def initialize_epsilon_closure(self) -> dict:
        epsilon_closure = {}
        for state in self.__states:
            epsilon_closure[state] = state
        return epsilon_closure


    def check_accept_state(self, transition: list) -> None:
        states = transition.split(',')
        for state in states:
            if state in self.__accept_states and transition not in self.__accept_states:
                self.__accept_states.append(transition)


    def clean_accept_states(self) -> None:
        for accept_state in self.__accept_states:
            if accept_state not in self.__states:
                self.__accept_states.remove(accept_state)


    def define_new_transitions(self, epsilon_closure: dict, transitions: dict) -> None:
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
                        self.check_accept_state(state_to_transit)
    
                    # Se o estado não houver transição, define ela como '-'.
                    if not state_to_transit:
                        state_to_transit = '-'
    
                    # Atualiza a transição.
                    self.__transitions[state][i] = state_to_transit
        # Retira os estados de aceitação que não fazem mais parte dos estados.
        self.clean_accept_states()


    # def negate(self) -> None:
    #     new_accept_states = []
    #     for state in self.states:
    #         if state not in self.__accept_states:
    #             new_accept_states.append(state)
    #     self.__accept_states = new_accept_states


    def display(self) -> None:
        print('Estados: ', ' | '.join(self.__states))
        print('Estados de aceitação: ', ' | '.join(self.__accept_states))
        print('Estado inicial: %s' % self.__initial_state)
        print('Alfabeto: ', ' | '.join(self.__alphabet))
        print('Transições:')
        for state, transition in self.__transitions.items():
            print(f'{state} -> {" | ".join(transition)}')


    def export(self, filename: str):
        text = f'#FA\n#States\n' +\
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


    # def recognize(self, sentence):
    #     self.NFA_to_FA()
    #     if not all([c in self.__alphabet for c in sentence]):
    #         return False

    #     current_state = self.__initial_state
    #     for c in sentence:
    #         i = self.__alphabet.index(c)
    #         current_state = self.__transitions[current_state][i]

    #     return current_state in self.__accept_states


    def minimize(self) -> None:
        # Determiniza.
        self.NFA_to_FA()
        # Remove estados inalcançáveis.
        self.remove_unreachable_states()
        # Remove estados mortos.
        self.remove_dead_states()
        # Junta estados equivalentes.
        self.unite_equivalent_states()


    def remove_unreachable_states(self) -> None:
        reachable_states_list = [self.__initial_state]
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


    def remove_dead_states(self) -> None:
        alive_states = self.__accept_states
        for state in self.__states:
            new_alive_states = []
            transitions = self.__transitions[state]
            for transition_state in transitions:
                if ((transition_state in alive_states) and 
                    (state not in alive_states) and 
                    (state not in new_alive_states) and 
                    (transition_state != '-')):
                    new_alive_states.append(state)
            alive_states.extend(new_alive_states)

        self.__states = list(set(self.__states).intersection(alive_states))
        self.__transitions = {s: t for s, t in self.__transitions.items() if s in alive_states}
        self.__transitions = {s: [t if t in alive_states else '-' for t in ts] for s, ts in self.__transitions.items()}


    def unite_equivalent_states(self) -> None:
        pass
