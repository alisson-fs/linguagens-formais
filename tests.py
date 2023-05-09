from file import File
from finite_automata import FiniteAutomata


# Determinização.
file = File('AFND.txt')
automata = file.read_file()
automata.NFA_to_FA()
automata.display()
