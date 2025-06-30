"""
Analizador Sintáctico para Little English
Paradigmas de Programación - Proyecto Programado 1
"""

from typing import List
from lexical_analyzer import Token, TokenType

class SyntaxAnalyzer:
    """Analizador Sintáctico para Little English usando Recursive Descent Parsing"""
    
    def __init__(self):
        self.tokens = []
        self.current_token_index = 0
        self.current_token = None
    
    def analyze(self, tokens: List[Token]) -> bool:
        """
        Realiza el análisis sintáctico de una lista de tokens
        
        Gramática de Little English:
        <sentence> ::= <noun_phrase> <verb_phrase> '.'
        <noun_phrase> ::= <article> <noun> | <article> <adjective> <noun>
        <verb_phrase> ::= <verb> | <verb> <noun_phrase> | <verb> <prep_phrase>
        <prep_phrase> ::= <preposition> <noun_phrase>
        
        Args:
            tokens: Lista de tokens del análisis léxico
            
        Returns:
            True si la oración es sintácticamente correcta
            
        Raises:
            SyntaxError: Si hay errores sintácticos
        """
        if not tokens:
            raise SyntaxError("Lista de tokens vacía")
        
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None
        
        try:
            # Comenzar con la regla principal
            self.parse_sentence()
            
            # Verificar que se hayan consumido todos los tokens
            if self.current_token_index < len(self.tokens):
                raise SyntaxError(f"Tokens adicionales después del punto: {self.current_token.value}")
            
            return True
            
        except (SyntaxError, IndexError) as e:
            if isinstance(e, IndexError):
                raise SyntaxError("Oración incompleta")
            raise e
    
    def consume_token(self, expected_type: TokenType = None):
        """
        Consume el token actual y avanza al siguiente
        
        Args:
            expected_type: Tipo de token esperado (opcional)
            
        Raises:
            SyntaxError: Si el token no es del tipo esperado
        """
        if self.current_token is None:
            raise SyntaxError("Token inesperado: fin de oración")
        
        if expected_type and self.current_token.type != expected_type:
            raise SyntaxError(f"Se esperaba {expected_type.value}, pero se encontró {self.current_token.type.value}: '{self.current_token.value}'")
        
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None
    
    def parse_sentence(self):
        """
        Parsea una oración completa
        <sentence> ::= <noun_phrase> <verb_phrase> '.'
        """
        self.parse_noun_phrase()
        self.parse_verb_phrase()
        self.consume_token(TokenType.DOT)
    
    def parse_noun_phrase(self):
        """
        Parsea una frase nominal
        <noun_phrase> ::= <article> <noun> | <article> <adjective> <noun>
        """
        # Debe comenzar con un artículo
        self.consume_token(TokenType.ARTICLE)
        
        # Verificar si hay un adjetivo
        if self.current_token and self.current_token.type == TokenType.ADJECTIVE:
            self.consume_token(TokenType.ADJECTIVE)
        
        # Debe terminar con un sustantivo
        self.consume_token(TokenType.NOUN)
    
    def parse_verb_phrase(self):
        """
        Parsea una frase verbal
        <verb_phrase> ::= <verb> | <verb> <noun_phrase> | <verb> <prep_phrase>
        """
        # Debe comenzar con un verbo
        self.consume_token(TokenType.VERB)
        
        # Verificar si hay una frase preposicional o nominal después del verbo
        if self.current_token and self.current_token.type == TokenType.PREPOSITION:
            self.parse_prep_phrase()
        elif self.current_token and self.current_token.type == TokenType.ARTICLE:
            self.parse_noun_phrase()
        # Si no hay nada más, es un verbo intransitivo (válido)
    
    def parse_prep_phrase(self):
        """
        Parsea una frase preposicional
        <prep_phrase> ::= <preposition> <noun_phrase>
        """
        self.consume_token(TokenType.PREPOSITION)
        self.parse_noun_phrase()

def test_syntax_analyzer():
    """Función de prueba para el analizador sintáctico"""
    from lexical_analyzer import LexicalAnalyzer
    
    lexical_analyzer = LexicalAnalyzer()
    syntax_analyzer = SyntaxAnalyzer()
    
    test_sentences = [
        "the cat runs.",                    # Válida: NP VP .
        "a big dog walks.",                 # Válida: NP(con adj) VP .
        "the man reads a book.",            # Válida: NP VP NP .
        "the cat runs in the house.",       # Válida: NP VP PP .
        "a small cat sleeps on the tree.",  # Válida: NP VP PP .
        "the cat.",                         # Inválida: falta VP
        "runs the cat.",                    # Inválida: orden incorrecto
        "the big cat runs quickly."         # Inválida: adverbio no está en gramática
    ]
    
    for sentence in test_sentences:
        print(f"Analizando: '{sentence}'")
        try:
            # Análisis léxico
            tokens = lexical_analyzer.analyze(sentence)
            print("Análisis léxico: EXITOSO")
            
            # Análisis sintáctico
            is_valid = syntax_analyzer.analyze(tokens)
            print("Análisis sintáctico: EXITOSO")
            
        except ValueError as e:
            print(f"Error léxico: {e}")
        except SyntaxError as e:
            print(f"Error sintáctico: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        print()

if __name__ == "__main__":
    test_syntax_analyzer()