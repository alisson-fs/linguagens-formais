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
        epsilon_closure, has_epsilon_closure = self.calculate_epsilon_closure()

        if epsilon_closure[self.__initial_state] != self.__initial_state:
            self.__initial_state = epsilon_closure[self.__initial_state]
            self.check_accept_state(self.__initial_state)

        if has_epsilon_closure:
            self.__states = [self.__initial_state]
            self.__transitions = {self.__initial_state: [None] * len(self.__alphabet)}
        else:
            self.__transitions = {}
            for state in self.__states:
                self.__transitions[state] = [None] * len(self.__alphabet)

        self.define_new_transitions(epsilon_closure, transitions)

    def calculate_epsilon_closure(self) -> tuple[dict, bool]:
        epsilon_closure = self.initialize_epsilon_closure()
        for state in self.__states:
            states = []
            alphabet_size = len(self.__alphabet)
            try:
                transition = self.__transitions[state][alphabet_size]
            except IndexError:
                return (epsilon_closure, False)
            else:
                states.append(state)
                if (transition != '-'):
                    transition = transition.split(',')
                    states.extend(transition)
                    states.sort()
                    epsilon_closure[state] = ','.join(set(map(str, states)))
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

    def clean_accept_states(self):
        for accept_state in self.__accept_states:
            if accept_state not in self.__states:
                self.__accept_states.remove(accept_state)

    def define_new_transitions(self, epsilon_closure: dict, transitions: dict) -> None:
        for state in self.__states:
            for i in range(len(self.__alphabet)):
                if self.__transitions[state][i] == None:
                    state_list = state.split(',')
    
                    state_list_for_transitions = []
                    for state in state_list:
                        state_list_for_transitions.append(
                            transitions[state][i])
    
                    state_to_transition = []
                    for state_transicao in state_list_for_transitions:
                        if (state_transicao != '-'):
                            if (len(state_transicao.split(',')) > 1):
                                state_transicao = state_transicao.split(',')
                                for e in state_transicao:
                                    state_to_transition.extend(
                                        epsilon_closure[e].split(','))
                            else:
                                state_to_transition.extend(
                                    epsilon_closure[state_transicao].split(','))
    
                    state_to_transition = list(set(state_to_transition))
                    state_to_transition.sort()
                    state_to_transition = ','.join(map(str, state_to_transition))
    
                    if state_to_transition not in self.__states and state_to_transition:
                        self.__states.append(state_to_transition)
                        self.__transitions[state_to_transition] = [None] * len(self.__alphabet)
                        self.check_accept_state(state_to_transition)
    
                    if not state_to_transition:
                        state_to_transition = '-'
    
                    self.__transitions[state][i] = state_to_transition
        self.clean_accept_states()

    def negate(self) -> None:
        new_accept_states = []
        for state in self.states:
            if state not in self.__accept_states:
                new_accept_states.append(state)
        self.__accept_states = new_accept_states

    def display(self) -> None:
        print('Estados (K): ', ' | '.join(self.__states))
        print('Estados de aceitação (F): ', ' | '.join(self.__accept_states))
        print('Estado inicial (q0): %s' % self.__initial_state)
        print('Alfabeto: ', ' | '.join(self.__alphabet))
        print('Transições:')
        for state, transition in self.__transitions.items():
            print(f'{state} -> {" | ".join(transition)}')

    def export(self, filename: str):
        text = f'*AF\n*Estados\n' +\
            f'{" ".join(self.__states)}\n' + \
            f'*EstadoInicial\n{self.__initial_state}\n' + \
            '*EstadosDeAceitacao\n' +\
            f'{" ".join(self.__accept_states)}\n' +\
            '*Alfabeto\n' +\
            f'{" ".join(self.__alphabet)}\n' + \
            '*Transicoes\n'

        for transition in self.__transitions.values():
            text += ' '.join(transition) + '\n'

        with open(filename, 'w') as file:
            file.write(text)

    def recognize(self, sentence):
        self.NFA_to_FA()
        if not all([c in self.__alphabet for c in sentence]):
            return False

        current_state = self.__initial_state
        for c in sentence:
            i = self.__alphabet.index(c)
            current_state = self.__transitions[current_state][i]

        return current_state in self.__accept_states
