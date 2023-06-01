from finite_automata_file import FiniteAutomataFile
from finite_automata import FiniteAutomata
from regular_expression_file import RegularExpressionFile
from utils import automata_union, automata_intersection


# Determinização sem Epsilon:
# file_nfa = FiniteAutomataFile('automatas/NFA.txt')
# fa = file_nfa.read_file()
# fa.NFA_to_FA()
# fa.export('automatas/FA.txt')
# fa.display()


# Determinização com Epsilon:
# file_nfa_with_epsilon = FiniteAutomataFile('automatas/NFA_with_epsilon.txt')
# fa_with_epsilon = file_nfa_with_epsilon.read_file()
# fa_with_epsilon.NFA_to_FA()
# fa_with_epsilon.export('automatas/FA_with_epsilon.txt')
# fa_with_epsilon.display()


# Minimização:
# file_nfa_to_minimize = FiniteAutomataFile('automatas/NFA_to_minimize.txt')
# fa_to_minimize = file_nfa_to_minimize.read_file()
# fa_to_minimize.minimize()
# fa_to_minimize.export('automatas/FA_minimum.txt')
# fa_to_minimize.display()


# União:
# file_fa_even_sum = FiniteAutomataFile('automatas/FA_even_sum.txt')
# fa_even_sum = file_fa_even_sum.read_file()
# file_fa_sum_mod_3 = FiniteAutomataFile('automatas/FA_sum_mod_3.txt')
# fa_sum_mod_3 = file_fa_sum_mod_3.read_file()
# nfa_union_fa_even_sum_and_fa_sum_mod_3, _, _ = automata_union(fa_even_sum, fa_sum_mod_3, convert_nfa_to_fa=False)
# nfa_union_fa_even_sum_and_fa_sum_mod_3.export('automatas/NFA_union_FA_even_sum_and_FA_sum_mod_3.txt')
# nfa_union_fa_even_sum_and_fa_sum_mod_3.display()
# fa_union_fa_even_sum_and_fa_sum_mod_3, _, _ = automata_union(fa_even_sum, fa_sum_mod_3)
# fa_union_fa_even_sum_and_fa_sum_mod_3.export('automatas/FA_union_FA_even_sum_and_FA_sum_mod_3.txt')
# fa_union_fa_even_sum_and_fa_sum_mod_3.display()


# Interseção:
# file_fa_even_sum = FiniteAutomataFile('automatas/FA_even_sum.txt')
# fa_even_sum = file_fa_even_sum.read_file()
# file_fa_sum_mod_3 = FiniteAutomataFile('automatas/FA_sum_mod_3.txt')
# fa_sum_mod_3 = file_fa_sum_mod_3.read_file()
# fa_intersection_fa_even_sum_and_fa_sum_mod_3 = automata_intersection(fa_even_sum, fa_sum_mod_3)
# fa_intersection_fa_even_sum_and_fa_sum_mod_3.display()


# Reconhecimento de sentença em AF:
# file_fa_even_sum = FiniteAutomataFile('automatas/FA_even_sum.txt')
# fa_even_sum = file_fa_even_sum.read_file()
# print(fa_even_sum.recognize_sentence('111'))
# print(fa_even_sum.recognize_sentence('0101'))
# print(fa_even_sum.recognize_sentence('01a'))

# Conversão de ER para AFD:
file_regular_expression_1 = RegularExpressionFile('regular_expressions/regular_expression_1.txt')
regular_expression_1 = file_regular_expression_1.read_file()
fa_corresponding_regular_expression_1 = regular_expression_1.RE_to_NFA()
fa_corresponding_regular_expression_1.display()

file_regular_expression_2 = RegularExpressionFile('regular_expressions/regular_expression_2.txt')
regular_expression_2 = file_regular_expression_2.read_file()
fa_corresponding_regular_expression_2 = regular_expression_2.RE_to_NFA()
fa_corresponding_regular_expression_2.display()
