from context_free_grammar import ContextFreeGrammar
from context_free_grammar_file import ContextFreeGrammarFile
from finite_automata_file import FiniteAutomataFile
from finite_automata import FiniteAutomata
from regular_expression import RegularExpression
from regular_expression_file import RegularExpressionFile
from regular_grammar import RegularGrammar
from regular_grammar_file import RegularGrammarFile
from utils import automata_union, automata_intersection, RE_to_DFA, FA_to_RG, RG_to_FA


def get_automata() -> FiniteAutomata:
    while True:
        file = input('Digite o nome do arquivo do automato (com extensão): ')
        try:
            file_fa = FiniteAutomataFile('automatas/' + file)
            fa = file_fa.read_file()
            print()
            break
        except FileNotFoundError:
            print('ERRO: Nome de arquivo inválido.')
    return fa


def get_regular_grammar() -> RegularGrammar:
    while True:
        file = input('Digite o nome do arquivo da gramática regular (com extensão): ')
        try:
            file_rg = RegularGrammarFile('regular_grammar/' + file)
            rg = file_rg.read_file()
            print()
            break
        except FileNotFoundError:
            print('ERRO: Nome de arquivo inválido.')
    return rg


def get_regular_expression() -> RegularExpression:
    while True:
        file = input('Digite o nome do arquivo da expressão regular (com extensão): ')
        try:
            file_re = RegularExpressionFile('regular_expressions/' + file)
            re = file_re.read_file()
            print()
            break
        except FileNotFoundError:
            print('ERRO: Nome de arquivo inválido.')
    return re


def get_context_free_grammar() -> ContextFreeGrammar:
    while True:
        file = input('Digite o nome do arquivo da gramática livre de contexto (com extensão): ')
        try:
            file_cfg = ContextFreeGrammarFile('context_free_grammar/' + file)
            cfg = file_cfg.read_file()
            print()
            break
        except FileNotFoundError:
            print('ERRO: Nome de arquivo inválido.')
    return cfg


def operations_automata(fa: FiniteAutomata = None) -> None:
    while True:
        print('Operações:')
        print('1 - Mostrar')
        print('2 - Exportar')
        print('3 - Conversão AFND para AFD')
        print('4 - Conversão AFD para GR')
        print('5 - Minimização')
        print('6 - União')
        print('7 - Interseção')
        print('8 - Renomear estados')
        print('9 - Sair')
        print()

        while True:
            operation = int(input('Digite o número referente à operação que deseja executar: '))
            if operation >= 1 and operation <= 9:
                print()
                break
            print('ERRO: Número inválido, digite outro.')    

        if operation == 1:
            if not fa:
                fa = get_automata()  
            fa.display()
            print()
            
        elif operation == 2:
            if not fa:
                fa = get_automata() 
            file_name = input('Nome do arquivo (com extensão): ')
            fa.export('automatas/' + file_name)
            print()

        elif operation == 3:
            if not fa:
                fa = get_automata() 
            fa.NFA_to_DFA()
            print()
            
        elif operation == 4:
            if not fa:
                fa = get_automata() 
            rg = FA_to_RG(fa)
            operations_regular_grammar(rg)
            print()

        elif operation == 5:
            if not fa:
                fa = get_automata() 
            fa.minimize()
            print()

        elif operation == 6:
            fa1 = get_automata() 
            fa2 = get_automata() 
            fa, _, _ = automata_union(fa1, fa2, convert_nfa_to_dfa=False)
            print()

        elif operation == 7:
            fa1 = get_automata() 
            fa2 = get_automata() 
            fa = automata_intersection(fa1, fa2)
            print()

        elif operation == 8:
            fa._clean_automata()
            print()
            
        elif operation == 9:
            break


def operations_regular_grammar(rg: RegularGrammar = None) -> None:
    while True:
        print('Operações:')
        print('1 - Mostrar')
        print('2 - Exportar')
        print('3 - Conversão GR para AFND')
        print('4 - Sair')
        print()

        while True:
            operation = int(input('Digite o número referente à operação que deseja executar: '))
            if operation >= 1 and operation <= 4:
                print()
                break
            print('ERRO: Número inválido, digite outro.')    

        if operation == 1:
            if not rg:
                rg = get_regular_grammar()  
            rg.display()
            print()
            
        elif operation == 2:
            if not rg:
                rg = get_regular_grammar() 
            file_name = input('Nome do arquivo (com extensão): ')
            rg.export('regular_grammar/' + file_name)
            print()
            
        elif operation == 3:
            if not rg:
                rg = get_regular_grammar() 
            fa = RG_to_FA(rg)
            operations_automata(fa)

        elif operation == 4:
            break


def operations_regular_expression(re: RegularExpression = None) -> None:
    while True:
        print('Operações:')
        print('1 - Mostrar')
        print('2 - Exportar')
        print('3 - Conversão ER para AFD')
        print('4 - Sair')
        print()

        while True:
            operation = int(input('Digite o número referente à operação que deseja executar: '))
            if operation >= 1 and operation <= 4:
                print()
                break
            print('ERRO: Número inválido, digite outro.')    

        if operation == 1:
            if not re:
                re = get_regular_expression()  
            re.display()
            print()
            
        elif operation == 2:
            if not re:
                re = get_regular_expression() 
            file_name = input('Nome do arquivo (com extensão): ')
            re.export('regular_expressions/' + file_name)
            print()
            
        elif operation == 3:
            if not re:
                re = get_regular_expression() 
            fa = RE_to_DFA(re)
            operations_automata(fa)

        elif operation == 4:
            break


def operations_context_free_grammar(cfg: ContextFreeGrammar = None) -> None:
    while True:
        print('Operações:')
        print('1 - Mostrar')
        print('2 - Exportar')
        print('3 - Fatorar')
        print('4 - Eliminar recursão à esquerda')
        print('5 - Calcular Firsts')
        print('6 - Calcular Follows')
        print('7 - Construir tabela de análise do preditivo LL1')
        print('8 - Reconhecimento de sentença por preditivo LL1')
        print('9 - Sair')
        print()

        while True:
            operation = int(input('Digite o número referente à operação que deseja executar: '))
            if operation >= 1 and operation <= 9:
                print()
                break
            print('ERRO: Número inválido, digite outro.')    

        if operation == 1:
            if not cfg:
                cfg = get_context_free_grammar()  
            cfg.display()
            print()
            
        elif operation == 2:
            if not cfg:
                cfg = get_context_free_grammar() 
            file_name = input('Nome do arquivo (com extensão): ')
            cfg.export('context_free_grammar/' + file_name)
            print()
            
        elif operation == 3:
            if not cfg:
                cfg = get_context_free_grammar() 
            cfg.factor()
    
        elif operation == 4:
            if not cfg:
                cfg = get_context_free_grammar() 
            cfg.remove_left_recursion()

        elif operation == 5:
            if not cfg:
                cfg = get_context_free_grammar() 
            firsts = cfg.get_firsts()
            print(firsts)
            print()

        elif operation == 6:
            if not cfg:
                cfg = get_context_free_grammar() 
            follows = cfg.get_follows()
            print(follows)
            print()
            
        elif operation == 7:
            if not cfg:
                cfg = get_context_free_grammar() 
            analysis_table = cfg.create_LL1_analysis_table()
            cfg.show_LL1_analysis_table(analysis_table)
            print()

        elif operation == 8:
            sentence = input('Sentença: ')
            if not cfg:
                cfg = get_context_free_grammar() 
            valid_sentence = cfg.recognize_sentence_ll1(sentence)
            if valid_sentence:
                print('Sentença válida.')
            else:
                print('Sentença inválida.')
            print()

        elif operation == 9:
            break


def main() -> None:
    while True:
        print('Operações:')
        print('1 - Operações com Autômato Finito')
        print('2 - Operações com Gramática Regular')
        print('3 - Operações com Expressão Regular')
        print('4 - Operações com Gramática Livre de Contexto')
        print('5 - Sair')
        print()

        while True:
            operation = int(input('Digite o número referente à operação que deseja executar: '))
            if operation >= 1 and operation <= 5:
                break
            print('ERRO: Número inválido, digite outro.')

        if operation == 1:
            operations_automata()
        elif operation == 2:
            operations_regular_grammar()
        elif operation == 3:
            operations_regular_expression()
        elif operation == 4:
            operations_context_free_grammar()
        elif operation == 5:
            break


main()
