"""
Analizador Léxico para Little English
Paradigmas de Programación - Proyecto Programado 1
"""

import re
from enum import Enum
from typing import List, Tuple, NamedTuple

class TokenType(Enum):
    """Tipos de tokens para Little English"""
    ARTICLE = "ARTICLE"
    NOUN = "NOUN"
    VERB = "VERB"
    ADJECTIVE = "ADJECTIVE"
    PREPOSITION = "PREPOSITION"
    DOT = "DOT"
    UNKNOWN = "UNKNOWN"

class Token(NamedTuple):
    """Representación de un token"""
    type: TokenType
    value: str
    position: int

class LexicalAnalyzer:
    """Analizador Léxico para Little English"""
    
    def __init__(self):
        # Definición del vocabulario de Little English
        self.vocabulary = {
            # Artículos
            'a': TokenType.ARTICLE,
            'the': TokenType.ARTICLE,
            
            # Sustantivos
            'cat': TokenType.NOUN,
            'dog': TokenType.NOUN,
            'man': TokenType.NOUN,
            'woman': TokenType.NOUN,
            'boy': TokenType.NOUN,
            'girl': TokenType.NOUN,
            'book': TokenType.NOUN,
            'house': TokenType.NOUN,
            'car': TokenType.NOUN,
            'tree': TokenType.NOUN,
            
            # Verbos
            'runs': TokenType.VERB,
            'walks': TokenType.VERB,
            'reads': TokenType.VERB,
            'sees': TokenType.VERB,
            'likes': TokenType.VERB,
            'has': TokenType.VERB,
            'is': TokenType.VERB,
            'goes': TokenType.VERB,
            'comes': TokenType.VERB,
            'sleeps': TokenType.VERB,
            
            # Adjetivos
            'big': TokenType.ADJECTIVE,
            'small': TokenType.ADJECTIVE,
            'red': TokenType.ADJECTIVE,
            'blue': TokenType.ADJECTIVE,
            'happy': TokenType.ADJECTIVE,
            'sad': TokenType.ADJECTIVE,
            'old': TokenType.ADJECTIVE,
            'new': TokenType.ADJECTIVE,
            'good': TokenType.ADJECTIVE,
            'bad': TokenType.ADJECTIVE,
            
            # Preposiciones
            'in': TokenType.PREPOSITION,
            'on': TokenType.PREPOSITION,
            'at': TokenType.PREPOSITION,
            'to': TokenType.PREPOSITION,
            'with': TokenType.PREPOSITION,
            'by': TokenType.PREPOSITION,
            'from': TokenType.PREPOSITION,
            'under': TokenType.PREPOSITION,
            'over': TokenType.PREPOSITION,
            'near': TokenType.PREPOSITION
        }
    
    def tokenize(self, sentence: str) -> List[Token]:
        """
        Realiza el análisis léxico de una oración
        
        Args:
            sentence: Oración a analizar
            
        Returns:
            Lista de tokens identificados
            
        Raises:
            ValueError: Si se encuentra un token no reconocido
        """
        # Normalizar la oración: convertir a minúsculas y limpiar espacios
        sentence = sentence.strip()
        if not sentence:
            raise ValueError("Oración vacía")
        
        tokens = []
        position = 0
        
        # Dividir la oración en palabras y procesar cada una
        words = sentence.split()
        
        for i, word in enumerate(words):
            # Verificar si la palabra termina con punto
            if word.endswith('.'):
                # Separar la palabra del punto
                word_without_dot = word[:-1]
                
                # Procesar la palabra sin el punto
                if word_without_dot:
                    word_lower = word_without_dot.lower()
                    if word_lower in self.vocabulary:
                        token_type = self.vocabulary[word_lower]
                        tokens.append(Token(token_type, word_without_dot, position))
                    else:
                        raise ValueError(f"Token no reconocido: '{word_without_dot}' en posición {position}")
                
                # Agregar el token del punto
                tokens.append(Token(TokenType.DOT, '.', position + len(word_without_dot)))
                position += len(word)
            else:
                # Procesar palabra normal
                word_lower = word.lower()
                if word_lower in self.vocabulary:
                    token_type = self.vocabulary[word_lower]
                    tokens.append(Token(token_type, word, position))
                else:
                    raise ValueError(f"Token no reconocido: '{word}' en posición {position}")
                position += len(word)
            
            # Agregar espacio entre palabras (excepto para la última)
            if i < len(words) - 1:
                position += 1
        
        return tokens
    
    def analyze(self, sentence: str) -> List[Token]:
        """
        Método principal para el análisis léxico
        
        Args:
            sentence: Oración a analizar
            
        Returns:
            Lista de tokens
            
        Raises:
            ValueError: Si hay errores léxicos
        """
        try:
            return self.tokenize(sentence)
        except ValueError as e:
            raise ValueError(f"Error léxico: {str(e)}")

def test_lexical_analyzer():
    """Función de prueba para el analizador léxico"""
    analyzer = LexicalAnalyzer()
    
    test_sentences = [
        "the cat runs.",
        "a big dog walks.",
        "the man reads a book.",
        "invalid_word runs."  # Esta debería fallar
    ]
    
    for sentence in test_sentences:
        print(f"Analizando: '{sentence}'")
        try:
            tokens = analyzer.analyze(sentence)
            print("Tokens encontrados:")
            for token in tokens:
                print(f"  {token.type.value}: '{token.value}' (pos: {token.position})")
        except ValueError as e:
            print(f"  Error: {e}")
        print()

if __name__ == "__main__":
    test_lexical_analyzer()