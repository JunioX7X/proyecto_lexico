"""
Compilador Principal para Little English
Paradigmas de Programación - Proyecto Programado 1

Este programa realiza análisis léxico y sintáctico de oraciones en Little English,
procesando un archivo de entrada línea por línea y generando un reporte de resultados.
"""

import sys
import os
from typing import List, Tuple
from lexical_analyzer import LexicalAnalyzer, Token
from syntax_analyzer import SyntaxAnalyzer

class LittleEnglishCompiler:
    """Compilador principal que integra análisis léxico y sintáctico"""
    
    def __init__(self):
        self.lexical_analyzer = LexicalAnalyzer()
        self.syntax_analyzer = SyntaxAnalyzer()
        self.results = []
    
    def compile_sentence(self, sentence: str, line_number: int) -> Tuple[str, bool, str]:
        """
        Compila una oración individual
        
        Args:
            sentence: Oración a compilar
            line_number: Número de línea en el archivo
            
        Returns:
            Tupla con (oración, éxito, mensaje_error)
        """
        sentence = sentence.strip()
        
        # Verificar si la línea está vacía
        if not sentence:
            return sentence, False, "Línea vacía"
        
        try:
            # Fase 1: Análisis Léxico
            tokens = self.lexical_analyzer.analyze(sentence)
            
            # Fase 2: Análisis Sintáctico
            self.syntax_analyzer.analyze(tokens)
            
            # Si llegamos aquí, ambos análisis fueron exitosos
            return sentence, True, "Compilación exitosa"
            
        except ValueError as e:
            # Error en análisis léxico
            return sentence, False, f"Error léxico: {str(e)}"
            
        except SyntaxError as e:
            # Error en análisis sintáctico
            return sentence, False, f"Error sintáctico: {str(e)}"
            
        except Exception as e:
            # Error inesperado
            return sentence, False, f"Error inesperado: {str(e)}"
    
    def compile_file(self, input_filename: str, output_filename: str):
        """
        Compila todas las oraciones de un archivo
        
        Args:
            input_filename: Nombre del archivo de entrada
            output_filename: Nombre del archivo de salida
        """
        # Verificar que el archivo de entrada existe
        if not os.path.exists(input_filename):
            raise FileNotFoundError(f"El archivo de entrada '{input_filename}' no existe")
        
        # Leer y procesar el archivo línea por línea
        self.results = []
        
        try:
            with open(input_filename, 'r', encoding='utf-8') as input_file:
                lines = input_file.readlines()
                
                for line_number, line in enumerate(lines, 1):
                    sentence, success, message = self.compile_sentence(line, line_number)
                    self.results.append({
                        'line_number': line_number,
                        'sentence': sentence,
                        'success': success,
                        'message': message
                    })
        
        except IOError as e:
            raise IOError(f"Error al leer el archivo de entrada: {str(e)}")
        
        # Generar archivo de salida
        self.generate_output_file(output_filename)
    
    def generate_output_file(self, output_filename: str):
        """
        Genera el archivo de salida con los resultados de la compilación
        
        Args:
            output_filename: Nombre del archivo de salida
        """
        try:
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                # Escribir encabezado
                output_file.write("REPORTE DE COMPILACIÓN - LITTLE ENGLISH\n")
                output_file.write("=" * 50 + "\n\n")
                
                # Estadísticas generales
                total_lines = len(self.results)
                successful_lines = sum(1 for result in self.results if result['success'])
                failed_lines = total_lines - successful_lines
                
                output_file.write(f"ESTADÍSTICAS GENERALES:\n")
                output_file.write(f"Total de líneas procesadas: {total_lines}\n")
                output_file.write(f"Compilaciones exitosas: {successful_lines}\n")
                output_file.write(f"Compilaciones fallidas: {failed_lines}\n")
                output_file.write(f"Tasa de éxito: {(successful_lines/total_lines)*100:.1f}%\n\n")
                
                # Resultados detallados
                output_file.write("RESULTADOS DETALLADOS:\n")
                output_file.write("-" * 30 + "\n\n")
                
                for result in self.results:
                    output_file.write(f"Línea {result['line_number']}: ")
                    
                    if result['sentence'].strip():
                        output_file.write(f"'{result['sentence']}'\n")
                    else:
                        output_file.write("(línea vacía)\n")
                    
                    status = "✓ ÉXITO" if result['success'] else "✗ FALLO"
                    output_file.write(f"Estado: {status}\n")
                    
                    if not result['success']:
                        output_file.write(f"Error: {result['message']}\n")
                    
                    output_file.write("\n")
                
                # Resumen de errores
                if failed_lines > 0:
                    output_file.write("RESUMEN DE ERRORES:\n")
                    output_file.write("-" * 20 + "\n")
                    
                    lexical_errors = 0
                    syntax_errors = 0
                    other_errors = 0
                    
                    for result in self.results:
                        if not result['success']:
                            if 'léxico' in result['message']:
                                lexical_errors += 1
                            elif 'sintáctico' in result['message']:
                                syntax_errors += 1
                            else:
                                other_errors += 1
                    
                    output_file.write(f"Errores léxicos: {lexical_errors}\n")
                    output_file.write(f"Errores sintácticos: {syntax_errors}\n")
                    output_file.write(f"Otros errores: {other_errors}\n")
        
        except IOError as e:
            raise IOError(f"Error al escribir el archivo de salida: {str(e)}")

def main():
    """Función principal del programa"""
    # Verificar argumentos de línea de comandos
    if len(sys.argv) != 3:
        print("Uso: python main.py <archivo_entrada> <archivo_salida>")
        print("Ejemplo: python main.py oraciones.txt resultados.txt")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    # Crear compilador e iniciar procesamiento
    compiler = LittleEnglishCompiler()
    
    try:
        print(f"Iniciando compilación de '{input_filename}'...")
        compiler.compile_file(input_filename, output_filename)
        print(f"Compilación completada. Resultados guardados en '{output_filename}'")
        
        # Mostrar estadísticas básicas en consola
        total = len(compiler.results)
        successful = sum(1 for r in compiler.results if r['success'])
        print(f"\nEstadísticas: {successful}/{total} oraciones compiladas exitosamente")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error de E/O: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()