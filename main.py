from tests import tests, single_test, test_from_pairs
from utils import binaryToDecimal

import math

def test(is_single, device, entries, is_local):
	""" Função que executa um teste com os parâmetro definidos

    Parâmetros:
    	is_single(bool): Booleano que marca se a execução é única ou completa
    	device(str): Nome do device a ser utilizado
    	entries(int): Número de pares no teste
    	is_local(bool): Booleano que marca se a execução é local ou no backend da IBM
 
    """
	single_test(is_single, device, entries, is_local, 1000, 0.5)

def step_tests(start, end, shots, precision, is_local, device):
	""" Função que executa um conjunto de testes únicos com os parâmetros definidos

    Parâmetros:
    	start(int): Número de pares da execução inicial
    	end(int): Número de pares da execução final
		shots(int): Número de execuções em cada teste
		precision(float): Valor de 0 a 1 que marca a precisão mínima
			para um teste ser considerado de sucesso
		is_local(bool): Booleano que define se a execução é local
			ou no backend da IBM
		device(str): Nome do simulador ou computador quântico no qual
			o programa será executado
 
    """
	tests(start, end, shots, precision, 1, 0, 0, 0, is_local, device)

def complete_tests(start, end, shots, precision, is_local, device):
	""" Função que executa um conjunto de testes completos com os parâmetros definidos

    Parâmetros:
    	start(int): Número de pares da execução inicial
    	end(int): Número de pares da execução final
		shots(int): Número de execuções em cada teste
		precision(float): Valor de 0 a 1 que marca a precisão mínima
			para um teste ser considerado de sucesso
		is_local(bool): Booleano que define se a execução é local
			ou no backend da IBM
		device(str): Nome do simulador ou computador quântico no qual
			o programa será executado
 
    """
	tests(1, 0, 0, 0, start, end, shots, precision, is_local, device)

def full_tests(single_start, single_limit, single_shots, single_precision, complete_start, complete_limit, complete_shots, complete_precision, is_local, device):
	""" Função que executa conjunto de testes para execução única e execução completa
		do número incial de cláusulas atômicas até o limite informado

    Parâmetros:
    	single_start(int): Número de claúsulas atômicas inicial para a execução única
    	single_limit(int): Número de claúsulas atômicas máximo para a execução única
    	single_shots(int): Número de execuções do circuito em cada teste para a execução única
        single_precision(float):  Valor de 0 a 1 que que representa a precisão mínima para 
        	que uma execução única seja considerada um sucesso
        complete_start(int): Número de claúsulas atômicas inicial para a execução complete
        complete_limit(int): Número de claúsulas atômicas máximo para a execução completa
        complete_shots(int): Número de execuções do circuito em cada teste para a execução completa
 		complete_precision(float): Valor de 0 a 1 que que representa a precisão mínima para que uma 
 			execução completa seja considerada um sucesso
		is_local(bool): Booleano que marca se a execução é local ou no backend da IBM
		device(str): String com o nome do simulador utilizado

    """
	tests(single_start, single_limit, single_shots, single_precision, complete_start, complete_limit, complete_shots, complete_precision, is_local, device)

def exe():
	""" Função chamada pelo script exe.sh que lê do param.txt os parâmetros
		e realiza os testes
	"""

	# Abre arquivo
	f = open("param.txt", "r")


	# Lê parâmetros
	single_start = int(f.readline())
	single_limit = int(f.readline())
	single_shots = int(f.readline())
	single_precision = float(f.readline())
	complete_start = int(f.readline())
	complete_limit = int(f.readline())
	complete_shots = int(f.readline())
	complete_precision = float(f.readline())
	is_local = str(f.readline()).rstrip("\n")

	# Modificações para lidar com pequenas diferenças
	device = str(f.readline()).rstrip("\n")

	print(is_local)

	if is_local == "True":
		is_local = True
	else:
		is_local = False

	print(type(is_local))
	print(is_local)
	print(device)

	tests(single_start, single_limit, single_shots, single_precision, complete_start, complete_limit, complete_shots, complete_precision, is_local, device)

def input_sequent(sequent, shots, precision, is_local, device):
	""" Função que recebe um sequente e cria o circuito para guiar 
		aplicação das regras de R-tensor
	"""
	print("Hello")
	# Tira espaços desnecessários e transforma em lista
	sequent = sequent.replace(' ', '')
	sequent = sequent.replace('*', '')
	sides = sequent.split('=')
	left_side = list(sides[0])
	right_side = list(sides[1])
	
	print(left_side)
	print(right_side)

	left_index = 0
	pairs = []
	for left_element in left_side:
		if left_element.isalnum() == False:
			print(left_element) 
			print("Elementos inválidos no lado esquerdo. Utilizar somente caracteres alfanuméricos como cláusulas atômicas e * como o tensor.")
			exit()

		right_index = 0
		for right_element in right_side:
			if right_element.isalnum() == False:
				print("Elementos inválidos no lado direito. Utilizar somente caracteres alfanuméricos como cláusulas atômicas e * como o tensor.")
				exit()

			if right_element == left_element:
				new_pair = [left_index, right_index]
				pairs.append(new_pair)
				break

			right_index = right_index + 1

		left_index = left_index + 1

	print(pairs)

	result = test_from_pairs(pairs, shots, precision, is_local, device)

	print("Resultado:")
	print(result)

	# Calculo quantos dígitos tem cada passo
	n = math.ceil(math.log(len(pairs), 2))

	# Usa o resultado para verficar se o sequente é uma prova válida

	counted = 0

	while counted < len(pairs):
		print("Loop")
		current_start = len(result) - (counted + 1) * n 
		binary = result[current_start: current_start + n]
		print(current_start)
		print(binary)
		answer = binaryToDecimal(binary)
		print(answer)

		if left_side[answer] != right_side[counted]:
			print("Não é uma prova válida.")
			exit()

		counted = counted + 1

	if len(pairs) < len(left_side):
		print("Não é uma prova válida.")
		exit()

	print("Prova válida.")



#input_sequent("A * B * C = C * A * B", 1000, 0.5, True, "qasm_simulator")