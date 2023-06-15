from context_free_grammar_file import ContextFreeGrammarFile
from finite_automata_file import FiniteAutomataFile
from finite_automata import FiniteAutomata
from regular_expression_file import RegularExpressionFile
from regular_grammar_file import RegularGrammarFile
from utils import automata_union, automata_intersection, RE_to_NFA, FA_to_RG, RG_to_FA


# Determinização sem Epsilon:
# file_nfa = FiniteAutomataFile('automatas/NFA.txt')
# nfa = file_nfa.read_file()
# nfa.NFA_to_DFA()
# nfa.export('automatas/DFA.txt')
# nfa.display()


# Determinização com Epsilon:
# file_nfa_with_epsilon = FiniteAutomataFile('automatas/NFA_with_epsilon.txt')
# nfa_with_epsilon = file_nfa_with_epsilon.read_file()
# nfa_with_epsilon.NFA_to_DFA()
# nfa_with_epsilon.export('automatas/DFA_with_epsilon.txt')
# nfa_with_epsilon.display()


# Minimização:
# file_nfa_to_minimize = FiniteAutomataFile('automatas/NFA_to_minimize.txt')
# nfa_to_minimize = file_nfa_to_minimize.read_file()
# nfa_to_minimize.minimize()
# nfa_to_minimize.export('automatas/DFA_minimum.txt')
# nfa_to_minimize.display()


# União:
# file_dfa_even_sum = FiniteAutomataFile('automatas/DFA_even_sum.txt')
# dfa_even_sum = file_dfa_even_sum.read_file()
# file_dfa_sum_mod_3 = FiniteAutomataFile('automatas/DFA_sum_mod_3.txt')
# dfa_sum_mod_3 = file_dfa_sum_mod_3.read_file()
# nfa_union_dfa_even_sum_and_dfa_sum_mod_3, _, _ = automata_union(dfa_even_sum, dfa_sum_mod_3, convert_nfa_to_dfa=False)
# nfa_union_dfa_even_sum_and_dfa_sum_mod_3.export('automatas/NFA_union_DFA_even_sum_and_DFA_sum_mod_3.txt')
# nfa_union_dfa_even_sum_and_dfa_sum_mod_3.display()
# dfa_union_dfa_even_sum_and_dfa_sum_mod_3, _, _ = automata_union(dfa_even_sum, dfa_sum_mod_3)
# dfa_union_dfa_even_sum_and_dfa_sum_mod_3.export('automatas/DFA_union_DFA_even_sum_and_DFA_sum_mod_3.txt')
# dfa_union_dfa_even_sum_and_dfa_sum_mod_3.display()


# Interseção:
# file_dfa_even_sum = FiniteAutomataFile('automatas/DFA_even_sum.txt')
# dfa_even_sum = file_dfa_even_sum.read_file()
# file_dfa_sum_mod_3 = FiniteAutomataFile('automatas/DFA_sum_mod_3.txt')
# fa_sum_mod_3 = file_dfa_sum_mod_3.read_file()
# dfa_intersection_dfa_even_sum_and_dfa_sum_mod_3 = automata_intersection(dfa_even_sum, dfa_sum_mod_3)
# dfa_intersection_dfa_even_sum_and_dfa_sum_mod_3.display()


# Reconhecimento de sentença em AF:
# file_dfa_even_sum = FiniteAutomataFile('automatas/DFA_even_sum.txt')
# dfa_even_sum = file_dfa_even_sum.read_file()
# print(dfa_even_sum.recognize_sentence('111'))
# print(dfa_even_sum.recognize_sentence('0101'))
# print(dfa_even_sum.recognize_sentence('01a'))


# Conversão de ER para AFD:
# file_regular_expression_1 = RegularExpressionFile('regular_expressions/regular_expression_1.txt')
# regular_expression_1 = file_regular_expression_1.read_file()
# fa_corresponding_regular_expression_1 = RE_to_NFA(regular_expression_1)
# fa_corresponding_regular_expression_1.display()

# file_regular_expression_2 = RegularExpressionFile('regular_expressions/regular_expression_2.txt')
# regular_expression_2 = file_regular_expression_2.read_file()
# fa_corresponding_regular_expression_2 = RE_to_NFA(regular_expression_2)
# fa_corresponding_regular_expression_2.display()


# Conversão AFD para GR:
# file_dfa_sum_mod_3 = FiniteAutomataFile('automatas/DFA_sum_mod_3.txt')
# dfa_sum_mod_3 = file_dfa_sum_mod_3.read_file()
# rg_sum_mod_3 = FA_to_RG(dfa_sum_mod_3)
# rg_sum_mod_3.display()
# rg_sum_mod_3.export('regular_grammar/RG_sum_mod_3.txt')

# Conversão GR sem epsilon para AFND:
# file_rg_sum_mod_3 = RegularGrammarFile('regular_grammar/RG_sum_mod_3.txt')
# rg_sum_mod_3 = file_rg_sum_mod_3.read_file()
# fa_sum_mod_3 = RG_to_FA(rg_sum_mod_3)
# fa_sum_mod_3.display()

# Conversão GR com epsilon para AFND:
# file_rg_even_sum_with_epsilon = RegularGrammarFile('regular_grammar/RG_even_sum_with_epsilon.txt')
# rg_even_sum_with_epsilon = file_rg_even_sum_with_epsilon.read_file()
# fa_even_sum_with_epsilon = RG_to_FA(rg_even_sum_with_epsilon)
# fa_even_sum_with_epsilon.display()

# Fatoração de GLC sem loop:
# file_cfg_no_loop = ContextFreeGrammarFile('context_free_grammar/CFG_no_loop.txt')
# cfg_no_loop = file_cfg_no_loop.read_file()
# cfg_no_loop.factor()
# cfg_no_loop.display()

# TODO
# Fatoração de GLC com loop:

# Remover recursão a esquerda com apenas recursão direta:
# file_cfg_just_direct_left_recursion = ContextFreeGrammarFile('context_free_grammar/CFG_just_direct_left_recursion.txt')
# cfg_just_direct_left_recursion = file_cfg_just_direct_left_recursion.read_file()
# cfg_just_direct_left_recursion.remove_left_recursion()
# cfg_just_direct_left_recursion.display()

# Remover recursão a esquerda com recursão direta e indireta:
# file_cfg_with_direct_and_indirect_left_recursion = ContextFreeGrammarFile('context_free_grammar/CFG_with_direct_and_indirect_left_recursion.txt')
# cfg_with_direct_and_indirect_left_recursion = file_cfg_with_direct_and_indirect_left_recursion.read_file()
# cfg_with_direct_and_indirect_left_recursion.remove_left_recursion()
# cfg_with_direct_and_indirect_left_recursion.display()

