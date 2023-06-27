from finite_automata import FiniteAutomata


class FiniteAutomataFile:
    def __init__(self, file: str) -> None:
        self.__file = file


    def read_file(self) -> FiniteAutomata:
        file = open(self.__file)
        text = file.read().split('\n')
        file.close()
        return self._get_automata(text)


    def _get_automata(self, text: str) -> FiniteAutomata:
        states = self._get_states(text)
        alphabet = self._get_alphabet(text)
        transitions = self._get_transitions(text)
        initial_state = self._get_initial_state(text)
        accept_states = self._get_accept_states(text)
        return FiniteAutomata(states, alphabet, transitions, initial_state, accept_states)


    def _get_states(self, text: str) -> list:
        index = text.index('#States')
        return text[index + 1].split(' | ')


    def _get_initial_state(self, text) -> str:
        index = text.index('#InitialState')
        return text[index + 1]


    def _get_accept_states(self, text: str) -> list:
        index = text.index('#AcceptStates')
        return text[index + 1].split(' | ')


    def _get_alphabet(self, text: str) -> list:
        index = text.index('#Alphabet')
        alphabet = text[index + 1].split(' | ')
        if '-' in alphabet:
            alphabet.remove('-')
        return alphabet

    def _get_transitions(self, text: str) -> dict:
        index = text.index('#Transitions')
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
