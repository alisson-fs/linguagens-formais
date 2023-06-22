Universidade Federal de Santa Catarina
Departamento de Informática e Estatística
Integrantes: Alisson Fabra da Silva (19200409) e Eduardo Vinicius Betim (19203161)
Data: 28 de junho de 2023

Linguagem utilizada: Python

Estruturas de dados:

    - Autômato Finito: Criamos uma classe chamada FiniteAutomata onde temos os seguintes atributos:
        - states: uma lista que guarda os estados;
        - alphabet: uma lista que guarda os símbolos do alfabeto;
        - transitions: um dicionário que possui os estados como chaves e uma lista dos estados destino como valores;
        - initial_state: guarda o estado inicial;
        - accept_states: uma lista com os estados de aceitação.

    - Gramática Regular: Criamos uma classe RegularGrammar que contém os atributos:
        - non_terminals: uma lista que guarda os símbolos não terminais;
        - terminals: uma lista que guarda os símbolos terminais;
        - productions: uma lista que guarda as produções;
        - initial_symbol: guarda o símbolo inicial.


    - Expressão Regular: Para a lógica de expressões regulares criamos duas classes, sendo elas RegularExpression e Node. Isso porque precisávamos fazer a conversão de expressões regulares para autômato finito utilizando o algoritmo baseado em árvore sintática. Sendo assim, a classe RegularExpression possui os atributos:
        - expression: uma string que guarda a expressão regular;
        - root: Node raiz da expressão regular no formato de árvore sintática;
        - indexes: guarda os índices das folhas da árvore sintática;
        - alphabet: uma lista com os símbolos do alfabeto;
        - index_to_symbol: um dicionário que possui os índices das folhas como chaves e os símbolos equivalentes como valores.

        A classe Node representa um nó da árvore sintática e possui os seguintes atributos:
        - c1: Node filho esquerdo;
        - c2: Node filho direito;
        - operation: operação que aquele nó da árvore sintática possui;
        - symbol: símbolo que aquele nó da árvore sintática possui;
        - index: indice que aquele nó da árvore sintática possui.

    - Gramática Livre de Contexto: Criamos uma classe chamada ContextFreeGrammar que contém os atributos:
        - non_terminals: uma lista que guarda os símbolos não terminais;
        - terminals: uma lista que guarda os símbolos terminais;
        - productions: um dicionário que possui os não terminais como chaves e uma lista das produções como valores;
        - initial_symbol: guarda o símbolo inicial.

Detalhes sobre o uso da aplicação:

    - Formato de entrada dos arquivos:
        - Existem 4 pastas para armazenar os arquivos referentes às estruturas do trabalho, que são automatas, regular_grammar, regular_expressions, context_free_grammar. Essas pastas guardam arquivos de Autômatos Finitos, Gramáticas Regulares, Expressões Regulares e Gramáticas Livres de Contexto, respectivamente. Esses arquivos devem ter os formatos mostrados abaixo, não deixando linhas em branco e nem espaços em branco no final de cada linha.

        - Autômato Finito:
        #FA
        #States
        A | B | C
        #InitialState
        A
        #AcceptStates
        A
        #Alphabet
        0 | 1
        #Transitions
        A -> A | B
        B -> B | C
        C -> C | A

        - Gramática Regular:
        #RG
        #NonTerminals
        S' | S | A | B
        #Terminals
        0 | 1
        #InitialSymbol
        S'
        #Productions
        S' -> 0S
        S' -> 0
        S' -> 1A
        S' -> &
        S -> 0S
        S -> 0
        S -> 1A
        A -> 0A
        A -> 1B
        B -> 0B
        B -> 1S
        B -> 1

        - Expressão Regular:
        #RE
        #Expression
        a.(a|b)*.a

        - Gramática Livre de Contexto:
        #CFG
        #NonTerminals
        E | E' | T | T' | F
        #Terminals
        id | + | * | ( | )
        #InitialSymbol
        E
        #Productions
        E -> TE'
        E' -> +TE'
        E' -> &
        T -> FT'
        T' -> *FT'
        T' -> &
        F -> (E)
        F -> id

    - Arquivo main:

        - O arquivo principal do programa. Ele fornece uma interface textual via terminal para que o usuário consiga decidir quais operações quer fazer. Ao escolher uma operação, o programa pede que o usuário informe o nome do arquivo que deseja utilizar, seja ele autômato, gramática etc.

    - Arquivo tests:

        - Esse arquivo possui alguns testes realizados durante a implementação das funcionalidades para sabermos se o que foi feito estava funcionando ou não. Por conta disso, existem testes de todos os tópicos solicitados no trabalho.

    - Arquivo utils:

        - Um dos motivos da criação do arquivo utils foram as operações de conversão de uma estrutura para outra, pois se fizéssemos as operações dentro das classes das estruturas acabava ocorrendo importação circular entre as classes. Por exemplo, na conversão de Autômato Finito para Gramática Regular era necessário importar a classe do Autômato Finito na Gramática Regular e vice-versa. O outro motivo que tivemos foi para fazer operações como união e interseção de autômatos que eram necessários dois para fazer.
