from regular_expression import RegularExpression


class RegularExpressionFile:
    def __init__(self, file: str) -> None:
        self.__file = file

    def read_file(self) -> RegularExpression:
        text = None
        try:
            file = open(self.__file)
            text = file.read().split('\n')
            file.close()
        except OSError:
            file.close()
        return self._get_regular_expression(text)

    def _get_regular_expression(self, text) -> RegularExpression:
        expression = self._get_expression(text)
        return RegularExpression(expression)

    def _get_expression(self, text: str) -> str:
        index = text.index('#Expression')
        return text[index+1]
