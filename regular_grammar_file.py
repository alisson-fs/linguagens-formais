from regular_grammar import RegularGrammar


class RegularGrammarFile:
    def __init__(self, file: str) -> None:
        self.__file = file


    def read_file(self) -> RegularGrammar:
        file = open(self.__file)
        text = file.read().split('\n')
        file.close()
        return self._get_regular_grammar(text)


    def _get_regular_grammar(self, text: str) -> RegularGrammar:
        non_terminals = self._get_non_terminals(text)
        terminals = self._get_terminals(text)
        productions = self._get_productions(text)
        initial_symbol = self._get_initial_symbol(text)
        return RegularGrammar(non_terminals, terminals, productions, initial_symbol)


    def _get_non_terminals(self, text: str) -> list:
        index = text.index('#NonTerminals')
        return text[index + 1].split(' | ')


    def _get_terminals(self, text) -> list:
        index = text.index('#Terminals')
        return text[index + 1].split(' | ')


    def _get_productions(self, text: str) -> list:
        index = text.index('#Productions')
        productions_list = text[index + 1:]
        grammar_productions = []
        for production in productions_list:
            grammar_productions.append(production)
        return grammar_productions


    def _get_initial_symbol(self, text: str) -> str:
        index = text.index('#InitialSymbol')
        return text[index + 1]
