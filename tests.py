from file import File
from finite_automata import FiniteAutomata


# Determinização.
# Sem Epsilon.
# file_NFA = File('automatas/NFA.txt')
# fa = file_NFA.read_file()
# fa.NFA_to_FA()
# fa.export('automatas/FA.txt')
# fa.display()

# Com Epsilon.
# file_NFA_with_epsilon = File('automatas/NFA_with_epsilon.txt')
# fa_with_epsilon = file_NFA_with_epsilon.read_file()
# fa_with_epsilon.NFA_to_FA()
# fa_with_epsilon.export('automatas/FA_with_epsilon.txt')
# fa_with_epsilon.display()


# Minimização
file_NFA_to_minimize = File('automatas/NFA_to_minimize.txt')
fa_to_minimize = file_NFA_to_minimize.read_file()
# automata_to_minimize.minimize()
fa_to_minimize.NFA_to_FA()
# fa_to_minimize.remove_unreachable_states()
fa_to_minimize.remove_dead_states()
# automata_to_minimize.export('automatas/FA_minimum.txt')
fa_to_minimize.display()