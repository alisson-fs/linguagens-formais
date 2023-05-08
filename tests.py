from File import File
from FiniteAutomata import FiniteAutomata


# Determinização.
file = File('AFND.txt')
automata = file.read_file()
automata.NFA_to_FA()
automata.display()