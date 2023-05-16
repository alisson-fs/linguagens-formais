from file import File
from finite_automata import FiniteAutomata


# Determinização.
# Sem Epsilon.
# file = File('NFA.txt')
# automata = file.read_file()
# automata.NFA_to_FA()
# automata.export('FA.txt')
# automata.display()

# Com Epsilon.
file = File('NFA_with_epsilon.txt')
automata_with_epsilon = file.read_file()
automata_with_epsilon.NFA_to_FA()
automata_with_epsilon.export('FA_with_epsilon.txt')
automata_with_epsilon.display()
