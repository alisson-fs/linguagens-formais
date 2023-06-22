from context_free_grammar import ContextFreeGrammar


class ContextFreeGrammarFile:
    def __init__(self, file: str) -> None:
        self.__file = file


    def read_file(self) -> ContextFreeGrammar:
        file = open(self.__file)
        text = file.read().split('\n')
        file.close()
        return self._get_context_free_grammar(text)


    def _get_context_free_grammar(self, text: str) -> ContextFreeGrammar:
        non_terminals = self._get_non_terminals(text)
        terminals = self._get_terminals(text)
        productions = self._get_productions(text)
        initial_symbol = self._get_initial_symbol(text)
        return ContextFreeGrammar(non_terminals, terminals, productions, initial_symbol)


    def _get_non_terminals(self, text: str) -> list:
        index = text.index('#NonTerminals')
        return text[index + 1].split(' | ')


    def _get_terminals(self, text) -> list:
        index = text.index('#Terminals')
        return text[index + 1].split(' | ')


    def _get_productions(self, text: str) -> list:
        index = text.index('#Productions')
        productions_list = text[index + 1:]
        grammar_productions = {}
        for production in productions_list:
            production_split = production.split(' -> ')
            non_terminal = production_split[0]
            production_non_terminal = production_split[1]
            if non_terminal not in grammar_productions.keys():
                grammar_productions[non_terminal] = []
            grammar_productions[non_terminal].append(production_non_terminal)
        return grammar_productions


    def _get_initial_symbol(self, text: str) -> str:
        index = text.index('#InitialSymbol')
        return text[index + 1]
