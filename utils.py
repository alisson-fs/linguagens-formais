from finite_automata import FiniteAutomata


def automata_union(automata_A: FiniteAutomata, automata_B: FiniteAutomata) -> FiniteAutomata:
    # Inicializando novos estados.
    n_states_A = len(automata_A.states)
    n_states_B = len(automata_B.states)
    new_states = ['q' + str(i) for i in range(1, n_states_A + n_states_B + 1)]

    # Definindo um novo estado inicial.
    new_transitions = {}
    new_initial_state = 'q0'
    new_transitions[new_initial_state] = ['-'] * len(automata_A.alphabet)
    initial_state_A = new_states[0]
    initial_state_B = new_states[len(automata_A.states)]
    new_initial_state_transition = initial_state_A + ',' + initial_state_B
    new_transitions[new_initial_state].append(new_initial_state_transition)

    # Inicializando transições dos novos estados.
    for state in new_states:
        new_transitions[state] = []

    new_accept_states = []
    update_transitions(automata_A, new_transitions, new_states, 0, new_accept_states)
    update_transitions(automata_B, new_transitions, new_states, n_states_A, new_accept_states)
    update_epsilon_transitions(automata_A, new_transitions, new_states, 0)
    update_epsilon_transitions(automata_B, new_transitions, new_states, n_states_A)

    new_states.insert(0, new_initial_state)
    new_automata = FiniteAutomata(
        new_states, 
        automata_A.alphabet, 
        new_transitions, 
        new_initial_state, 
        new_accept_states
    )

    return new_automata
    

# Atualiza transições por simbolos do alfabeto com os estados do automato correspondente aos estados do automato original.
def update_transitions(
        automata: FiniteAutomata, 
        new_transitions: dict, 
        new_states: list, 
        base_index: int, 
        new_accept_states: list 
) -> None:
    j = base_index
    for state in automata.states:
        correspondent_state = new_states[j]
        for i in range(0, len(automata.alphabet)):
            transition = automata.transitions[state][i]
            if transition == '-':
                new_transitions[correspondent_state].append('-')
                continue
            new_transition = []
            for state_transition in transition.split(','):
                original_state_index = automata.states.index(state_transition)
                new_transition.append(new_states[original_state_index + base_index])
            new_transition = ','.join(map(str, new_transition))
            new_transitions[correspondent_state].append(new_transition)
            if state in automata.accept_states:
                new_accept_states.append(correspondent_state)
        j += 1


# Atualiza transições por epsilon com os estados do automato correspondente aos estados do automato original.
def update_epsilon_transitions(
        automata: FiniteAutomata,
        new_transitions: dict,
        new_states: list,
        base_index: int
) -> None:
    i = len(automata.alphabet)
    j = base_index
    for state in automata.states:
        correspondent_state = new_states[j]
        j += 1
        try:
            transition = automata.transitions[state][i]
        except IndexError:
            new_transitions[correspondent_state].append('-')
        else:
            if transition == '-':
                new_transitions[correspondent_state].append('-')
                continue
            new_transition = []
            for state_transition in transition.split(','):
                original_state_index = automata.states.index(state_transition)
                new_transition.append(new_states[original_state_index + base_index])
            new_transition = ','.join(map(str, new_transition))
            new_transitions[correspondent_state].append(new_transition)
