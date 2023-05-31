from finite_automata import FiniteAutomata


def automata_union(
        automata_A: FiniteAutomata, 
        automata_B: FiniteAutomata,
        convert_nfa_to_fa: bool = True
) -> tuple[FiniteAutomata, dict, dict]:
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
    automata_A.update_new_transitions(new_transitions, new_states, 0, new_accept_states)
    automata_B.update_new_transitions(new_transitions, new_states, n_states_A, new_accept_states)
    automata_A.update_new_epsilon_transitions(new_transitions, new_states, 0)
    automata_B.update_new_epsilon_transitions(new_transitions, new_states, n_states_A)

    new_states.insert(0, new_initial_state)
    new_automata = FiniteAutomata(
        new_states, 
        automata_A.alphabet, 
        new_transitions, 
        new_initial_state, 
        new_accept_states
    )

    equivalent_states_A = {automata_A.states[i]: new_states[i + 1] for i in range(0, n_states_A)}
    equivalent_states_B = {automata_B.states[i]: new_states[i + n_states_A + 1] for i in range(0, n_states_B)}

    if convert_nfa_to_fa:
        new_automata.NFA_to_FA()

    return new_automata, equivalent_states_A, equivalent_states_B


def automata_intersection(automata_A: FiniteAutomata, automata_B: FiniteAutomata) -> FiniteAutomata:
    # Faz a união dos automatos.
    union_automata_A_B, equivalent_states_A, equivalent_states_B = automata_union(automata_A, automata_B, convert_nfa_to_fa=True)

    # Caso o estado q0 criado na união faça transição por epsilon para o estado inicial dos automatos iniciais, 
    # inclui ele nos estados de aceitação.
    equivalent_accept_states_A = [equivalent_states_A[state] for state in automata_A.accept_states]
    if 'q1' in equivalent_accept_states_A:
        equivalent_accept_states_A.append('q0')
    equivalent_accept_states_B = [equivalent_states_B[state] for state in automata_B.accept_states]
    if 'q' + str(len(automata_A.states) + 1) in equivalent_accept_states_B:
        equivalent_accept_states_B.append('q0')

    # Retira os estados de aceitação que não são uma interseção com os estados de aceitação dos automatos iniciais.
    new_accept_states = []
    for accept_state in union_automata_A_B.accept_states:
        accept_separate_states = accept_state.split(',')
        initial_len_accept_separate_states = len(accept_separate_states)

        for state in accept_separate_states[:]:
            if state in equivalent_accept_states_A:
                accept_separate_states.remove(state)

        len_accept_separate_states = len(accept_separate_states)
        if (len_accept_separate_states == 0 or 
            len_accept_separate_states == initial_len_accept_separate_states):
            continue

        for state in accept_separate_states[:]:
            if state in equivalent_accept_states_B:
                accept_separate_states.remove(state)

        if len(accept_separate_states) == 0:
            new_accept_states.append(accept_state)

    union_automata_A_B.accept_states = new_accept_states
    union_automata_A_B.minimize(clean_automata=True)
    return union_automata_A_B
