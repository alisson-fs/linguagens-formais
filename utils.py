from finite_automata import FiniteAutomata
from regular_expression import RegularExpression
from regular_grammar import RegularGrammar


def automata_union(
        automata_A: FiniteAutomata, 
        automata_B: FiniteAutomata,
        convert_nfa_to_dfa: bool = True
) -> tuple[FiniteAutomata, dict, dict]:
    automata_A, automata_B = merge_alphabets(automata_A, automata_B)
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

    if convert_nfa_to_dfa:
        new_automata.NFA_to_DFA()

    return new_automata, equivalent_states_A, equivalent_states_B


def automata_intersection(automata_A: FiniteAutomata, automata_B: FiniteAutomata) -> FiniteAutomata:
    # Faz a união dos automatos.
    union_automata_A_B, equivalent_states_A, equivalent_states_B = automata_union(automata_A, automata_B, convert_nfa_to_dfa=True)

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


def RE_to_DFA(re: RegularExpression) -> FiniteAutomata:
    # Define o followpos.
    followpos = {i: set() for i in re.indexes}
    followpos = re.root.get_followpos(followpos)

    # Define o estado inicial.
    initial_state = str(re.root.get_firstpos())
    accept_states = []
    unchecked_target_states = [re.root.get_firstpos()]
    checked_target_states = []
    temp_transitions = []

    # Constroi a lógica de transições utilizando os indices do estado e o followpos para 
    # definir os estados destino para cada simbolo do alfabeto.
    while unchecked_target_states:
        current_state = unchecked_target_states.pop(0)
        checked_target_states.append(current_state)
        for alphabet_symbol in re.alphabet:
            next_state = set()
            for index_symbol in current_state:
                if re.index_to_symbol[index_symbol] == alphabet_symbol:
                    current_followpos = followpos[index_symbol]
                    next_state = next_state.union(current_followpos)

            if next_state and next_state not in checked_target_states:
                unchecked_target_states.append(next_state)

            current_temp_transition = {'state': current_state, 'symbol': alphabet_symbol, 'next': next_state}
            if next_state and current_temp_transition not in temp_transitions:
                if max(re.indexes) in current_temp_transition['state']:
                    accept_states.append(str(current_state))
                temp_transitions.append(current_temp_transition)

    # Define as transições por simbolo do alfabeto.
    transitions = {}
    for temp_transition in temp_transitions:
        current_state = str(temp_transition['state'])
        symbol = str(temp_transition['symbol'])
        next_state = str(temp_transition['next'])

        if current_state not in transitions.keys():
            transitions[current_state] = {}
        transitions[current_state][symbol] = next_state

    # Organiza as transições para o formato de entrada do automato definindo também as transições vazias.
    new_transitions = {}
    for state, transitions_state in transitions.items():
        transistions_ordered_by_symbol = []
        for alphabet_symbol in re.alphabet:
            if alphabet_symbol in transitions_state.keys():
                transistions_ordered_by_symbol.append(transitions_state[alphabet_symbol])
            else:
                transistions_ordered_by_symbol.append('-')
        new_transitions[state] = transistions_ordered_by_symbol

    return FiniteAutomata(
        states=list(new_transitions.keys()),
        alphabet=re.alphabet,
        initial_state=initial_state,
        accept_states=accept_states,
        transitions=new_transitions
    )


def FA_to_RG(fa: FiniteAutomata) -> RegularGrammar:
    # Mapeamento de estados para não terminais.
    correspondent_non_terminal = {}
    correspondent_non_terminal[fa.initial_state] = 'S'
    letter = 'A'
    for state in fa.states:
        if state == fa.initial_state:
            continue
        correspondent_non_terminal[state] = letter
        letter = chr(ord(letter) + 1)

    N = list(correspondent_non_terminal.values())
    T = fa.alphabet
    S = correspondent_non_terminal[fa.initial_state]
    P = []
    for state, state_transitions in fa.transitions.items():
        for state_transition, symbol in zip(state_transitions, fa.alphabet):
            if state_transition == '-':
                continue
            P.append(f'{correspondent_non_terminal[state]} -> {symbol}{correspondent_non_terminal[state_transition]}')
            if state_transition in fa.accept_states:
                P.append(f'{correspondent_non_terminal[state]} -> {symbol}')

    # Cria um novo estado inicial caso a gramática aceite epsilon.
    if fa.initial_state in fa.accept_states:
        # Criando um não terminal S' 
        S = correspondent_non_terminal[fa.initial_state] + "'"
        N.insert(0, S)
        new_S_productions = []
        # Adicionando as produções de S em S'.
        for production in P.copy():
            if production[0] == correspondent_non_terminal[fa.initial_state]:
                production_split = production.split(' -> ')
                new_S_productions.append(f'{S} -> {production_split[1]}')
        # Adicionando a produção de epsilon em S'.
        new_S_productions.append(f'{S} -> &')
        P = new_S_productions + P

    return RegularGrammar(N, T, P, S)


def RG_to_FA(rg: RegularGrammar) -> FiniteAutomata:
    # Define os estados do automato.
    states = rg.non_terminals
    letter = 'A'
    for _ in range(26):
        if letter not in rg.non_terminals:
            accept_state = letter
            states.append(accept_state)
            break
        letter = chr(ord(letter) + 1)
    # Define o alfabeto.
    alphabet = rg.terminals

    # Define o estado inicial.
    initial_state = rg.initial_symbol

    # Define os estados de aceitação.
    accept_states = [accept_state]

    # Define as transições do automato pelas produções da gramática.
    grammar_transitions = {}
    for production in rg.productions:
        current_state, terminal, non_terminal, has_epsilon_transition = rg.separate_production(production)

        # Se houver epsilon, adiciona a transição para o estado de aceitação.
        if has_epsilon_transition:
            if (current_state, '&') not in grammar_transitions.keys():
                grammar_transitions[(current_state, '&')] = []
            grammar_transitions[(current_state, '&')].append(accept_state)
        else:
            if (current_state, terminal) not in grammar_transitions.keys() and terminal is not None:
                grammar_transitions[(current_state, terminal)] = []
            if non_terminal is None and terminal is not None:
                grammar_transitions[(current_state, terminal)].append(accept_state)
            elif non_terminal is not None and terminal is not None:
                grammar_transitions[(current_state, terminal)].append(non_terminal)

    # Cria as transições para estados mortos.
    for non_terminal in rg.non_terminals:
        for terminal in rg.terminals:
            if (non_terminal, terminal) not in grammar_transitions.keys():
                grammar_transitions[(non_terminal, terminal)] = ['-']

    # Define as transições no formato de entrada do automato.
    temp_transitions = {}
    for non_terminal in rg.non_terminals:
        temp_transitions[non_terminal] = []
        for symbol in alphabet:
            if (non_terminal, symbol) in grammar_transitions.keys():
                temp_transitions[non_terminal].append(grammar_transitions[(non_terminal, symbol)])
            else:
                temp_transitions[non_terminal].append('-')
        if (non_terminal, '&') in grammar_transitions.keys():
            temp_transitions[non_terminal].append(grammar_transitions[(non_terminal, '&')])
        else:
            temp_transitions[non_terminal].append('-')

    # Arrumando os estados de destino das transições para o formato de entrada do automato.
    transitions = {}
    for state, next_states in temp_transitions.items():
        transitions[state] = []
        for next_state in next_states:
            next_state = ','.join(next_state)
            transitions[state].append(next_state)

    return FiniteAutomata(states, alphabet, transitions, initial_state, accept_states)


def merge_alphabets(automata_A: FiniteAutomata, automata_B: FiniteAutomata) -> tuple[FiniteAutomata, FiniteAutomata]:
    new_alphabet = automata_A.alphabet[:]
    equivalent_index_alphabet_B_to_new_alphabet = {}
    for symbol in automata_B.alphabet:
        if symbol not in automata_A.alphabet:
            new_alphabet.append(symbol)
        equivalent_index_alphabet_B_to_new_alphabet[automata_B.alphabet.index(symbol)] = new_alphabet.index(symbol)


    len_diff = len(new_alphabet) - len(automata_A.alphabet)
    for state_transitions in automata_A.transitions.keys():
        automata_A.transitions[state_transitions] += ['-'] * len_diff

    for state_transitions in automata_B.transitions.keys():
        temp_transitions = ['-'] * len(new_alphabet)    
        for symbol in automata_B.alphabet:
            index_symbol = automata_B.alphabet.index(symbol)
            temp_transitions[equivalent_index_alphabet_B_to_new_alphabet[index_symbol]] = automata_B.transitions[state_transitions][index_symbol]
        automata_B.transitions[state_transitions] = temp_transitions
    automata_A.alphabet = new_alphabet
    automata_B.alphabet = new_alphabet
    return automata_A, automata_B
