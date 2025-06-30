# 🚀 Compilador Little English - Proyecto Programado 1

Un compilador para un lenguaje minimalista llamado "Little English" que realiza análisis léxico y sintáctico de oraciones simples en inglés. Desarrollado para el curso de Paradigmas de Programación.

## 📚 Características

- **Análisis Léxico**: Identifica tokens como artículos, sustantivos, verbos, adjetivos y preposiciones.
- **Análisis Sintáctico**: Verifica la estructura gramatical de las oraciones.
- **Reportes Detallados**: Genera un archivo de salida con estadísticas y resultados de la compilación.
- **Manejo de Errores**: Detecta y reporta errores léxicos y sintácticos.

## 🛠️ Requisitos

- Python 3.8 o superior
- No se requieren librerías externas

## 🏃‍♂️ Cómo Ejecutarlo

1. **Clona el repositorio** (si aplica) o descarga los archivos:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd little-english-compiler

Prepara tu archivo de entrada:

Crea un archivo oraciones.txt con las oraciones que deseas analizar (una por línea).

Ejemplo:

the cat runs.
a big dog walks.
the man reads a book.


Revisa los resultados:

El compilador generará un archivo resultados.txt con el reporte detallado.


🧪 Ejemplos de Oraciones Válidas

the cat runs.
a big dog walks.
the man reads a book in the house.


🚫 Ejemplos de Oraciones Inválidas


cat the runs.          # Orden incorrecto
the big runs.          # Falta sustantivo
the cat runs quickly.  # Adverbio no soportado


📂 Estructura de Archivos

little-english-compiler/
├── main.py              # Programa principal
├── lexical_analyzer.py  # Analizador léxico
├── syntax_analyzer.py   # Analizador sintáctico
├── oraciones.txt        # Ejemplo de entrada
└── resultados.txt       # Ejemplo de salida


📊 Gramática de Little English

<sentence>      ::= <noun_phrase> <verb_phrase> '.'
<noun_phrase>   ::= <article> <noun> | <article> <adjective> <noun>
<verb_phrase>   ::= <verb> | <verb> <noun_phrase> | <verb> <prep_phrase>
<prep_phrase>   ::= <preposition> <noun_phrase>


🎨 Ejemplo Creativo
Imagina que estás enseñando inglés a una computadora. Little English es como un bebé robot que solo entende oraciones simples como:

"The happy boy sees a small cat in the house."

Pero se confunde con cosas complejas como:

"The boy who is happy sees the cat that is small."
