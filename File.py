from finite_automata import FiniteAutomata


class File:

    def __init__(self, file) -> None:
        self.__file = file

    def read_file(self):
        text = None
        try:
            file = open(self.__file)
            text = file.read().split('\n')
            file.close()
        except OSError:
            file.close()

        type = self.get_type(text)

        if (type == '*AF') : # Encontrou um automato finito
            return self.get_automata(text)
        # elif (type == '*GR' or type == '*GLC') : # Encontrou uma gramatica regular ou uma glc
        #     return self.read_gramatic(text, type)
        # elif (type == '*ER') : # Encontrou uma expressao regular
        #     return self.read_expression(text)
        # else:
        #     exit()

    def get_type(self, text) -> str:
        return text[0]

    def get_automata(self, text: str) -> FiniteAutomata:
        states = self.get_states(text)
        alphabet = self.get_alphabet(text)
        transitions = self.get_transitions(text)
        initial_state = self.get_initial_state(text)
        accept_states = self.get_accept_states(text)

        return FiniteAutomata(states, alphabet, transitions, initial_state, accept_states)

    def get_states(self, text: str) -> list:
        index = text.index('*Estados')
        return text[index + 1].split(' | ')

    def get_initial_state(self, text) -> str:
        index = text.index('*EstadoInicial')
        return text[index + 1]

    def get_accept_states(self, text: str) -> list:
        index = text.index('*EstadosDeAceitacao')
        return text[index + 1].split(' | ')

    def get_alphabet(self, text: str) -> list:
        index = text.index('*Alfabeto')
        return text[index + 1].split(' | ')

    def get_transitions(self, text: str) -> dict:
        index = text.index('*Transicoes')
        transitions_list = text[index + 1:]
        automata_transitions = {}
        for transitions in transitions_list:
            state_transitions = transitions.split(' -> ')
            state = state_transitions[0]
            transitions = state_transitions[1].split(' | ')
            automata_transitions[state] = []
            for state_to_transition in transitions:
                automata_transitions[state].append(state_to_transition)
        return automata_transitions
