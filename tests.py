# Código criado por Lorenzo Saraiva
###############  Módulo de testes  ############### 

from grover import grover_search_algorithm

from utils import to_bin
from operator import itemgetter

import time
import random
import math

def execute(entries, is_single, shots, threshold, is_local, device, pairs = []):
	"""Função que gera aleatoriamente um conjunto de pares e executa o Grover
	
	Parâmetros:
		entries (int): Número de pares na base de dados entrelaçada
		is_single(bool): Booleano que marca se é uma execução única ou completa
		shots(int): Número de execuções do circuito
		threshold(float): Valor de 0 a 1 que representa o valor de precisão mínima
			para que a execução seja considerada de sucesso
		is_local(bool): Booleano que marca se a execução é local ou no backend da IBM
		device(str): Nome do simulador ou computador quântico onde o código será 
			executado
	
	Retorno:
		float: Valor da precisão caso a execução acerte, ou 0 caso falhe.
	"""

	n = math.ceil(math.log(entries, 2)) # numero de qubits necessários

	# caso o número de pares não seja potência de 2, calcula a potência mais próxima
	power = 1;
	while power < entries:
		power = power * 2; 

	ceil = power ** 2 # valor máximo 

	# Geração de pares aleatórios para a database
	l1 = []
	l2 = []

	# Gera duas listas com valores 0 a 2^m
	for i in range(entries):
		l1.append(i)
		l2.append(i)

	# Embaralha as listas
	random.shuffle(l1)
	random.shuffle(l2)

	if len(pairs) == 0:
		# Cria os pares aleatórios
		for i in range(entries):
			a = l1.pop()
			b = l2.pop()
			pairs.append([a, b])

	# Calcula o índice de cada par no vetor de estado
	indexes = []


	for i in range(entries):
		indexes.append(pairs[i][0] * power + pairs[i][1])

	# Prepara o vetor de estados de acordo com os índices calculados
	initial_state = [0] * ceil

	for i in range(entries):
		initial_state[indexes[i]] = math.sqrt(1/entries)

	variables = entries

	if is_single:
		variables = 1

	target = random.randint(0, entries - 1)

	answer_dict = grover_search_algorithm(n, entries, initial_state, variables, target, shots, is_local, device)

	answer = compute_answer(answer_dict, pairs, is_single, target, n)

	# Pega o resultado mais frequente e sua frequência
	top_result = list(answer_dict.keys())[-1]
	accuracy = list(answer_dict.values())[-1]/shots

	# Caso seja correto, retorna a resposta e a precisão
	if top_result == answer:
		return accuracy, top_result
	else:
		return 0, False

def compute_answer(answer_dict, pairs, is_single, target, n):  	
	"""Função que verifica a resposta correta a partir dos pares
		para checar se a execução foi um sucesso
	
	Parâmetros:
		answer_dict(dict): Dicionário com os resultados da execução do circuito
		pairs([[int, int]]: Lista de pares que representam o sequente
		is_single(bool): Booleano que marca se é uma execução única ou completa
		target(int): Caso seja a execução única, qual será o par procurado
		n(int): Número de qubits em um lado da base de dados entrelaçada
	
	Retorno:
		bin: Resposta correta em binário

	"""

	# Verifica se é execução única
	if is_single:
		
		answer = -1

		# Procura o par que está sendo buscado
		for i in range(len(pairs)):
			pair = pairs[i]
			if pair[1] == target:
				answer = pair[0]

		return to_bin(answer, n)

	else:
		
		pairs = sorted(pairs, key=itemgetter(1))
		pairs.reverse()
		answer = ""

		# Computa a resposta correta
		for pair in pairs: 
			answer = answer + str(to_bin(pair[0], n))

		return answer

def tests(single_start, single_limit, single_shots, single_precision, complete_start, complete_limit, complete_shots, complete_precision, is_local, device):
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
		device(str): String com o nome do simulador ou computador quântico utilizado

	"""

	if validate_device(is_local, device) == False: 
		print("Device escolhido não é válido.")
		return

	f = open("test_results.txt", "a")

	
	# Testando um único passo do algoritmo, portanto podem ser feitos testes com mais qubits
	# Loop que testa execução singular aumentando gradualmente o número de qubits
	for atomics in range(single_start, single_limit + 1):

		start_time = time.time()

		result, answer = execute(atomics, True, single_shots, single_precision, is_local, device, [])
		
		execution_time = time.time() - start_time

		log(True, device, atomics, execution_time, single_shots, result, f, single_precision)
	
	
	# Testando o algoritmo completo 
	# Esses testes são limitados pela disponibilidade de computadores quânticos e/ou memória RAM para simular
	for atomics in range(complete_start, complete_limit + 1):

		start_time = time.time()
		
		result, answer = execute(atomics, False, complete_shots, complete_precision, is_local, device, [])
		
		execution_time = time.time() - start_time

		log(False, device, atomics, execution_time, complete_shots, result, f, complete_precision)
			
def single_test(is_single, device, entries, is_local, shots, precision):
	""" Função que executa um teste com os parâmetros definidos 

	Parâmetros:
		is_single(bool): Booleano que marca se a execução é única ou completa
		device(str): Nome do device a ser utilizado
		entries(int): Número de pares no teste
		is_local(bool): Booleano que marca se a execução é local ou no backend da IBM
		precision(float):  Valor de 0 a 1 que que representa a precisão mínima para 
			que uma execução seja considerada um sucesso
		shots(int): Número de execuções do circuito em cada teste 

	"""

	if validate_device(is_local, device) == False: 
		print("Device escolhido não é válido.")
		return


	f = open("test_results.txt", "a")

	start_time = time.time()

	result, answer = execute(entries, is_single, shots, precision, is_local, device)
	
	execution_time = time.time() - start_time

	log(is_single, device, entries, execution_time, shots, result, f, precision)
	
def log(is_single, device, entries, execution_time, shots, result, f, precision):
	""" Função que gera um log com os resultados do teste

	Parâmetros:
		is_single(bool): Booleano que marca se a execução é única ou completa
		device(str): Nome do device a ser utilizado
		qubits(int): Número de qubits no teste
		execution_time(float): Tempo em segundos que durou a execução
		shots(int): Número de execuções do circuito em cada teste 
		result(float): Frequência do resultado correto
		f(file): Arquivo de log

	"""
	execution_type = ""

	if is_single:
		execution_type = "única"
	else:
		execution_type = "completa"

	if result == 0:
		f.write("Erro na execução " + execution_type + " com " + str(entries) + "pares. Duração: " + str(round(execution_time, 3)) + " segundos. Device: " + device + "\n")
	elif result < precision:
		f.write(str(entries) + " pares " + execution_type + " Resultado correto porém precisão abaixo do limte. Precisão: " + str(result) + " Duração: " + str(round(execution_time, 3)) + " segundos. Device: " + device + "\n")
	else:
		f.write(str(entries) + " pares " + execution_type + " -- OK. Precisão: " + str(result) + " Duração: " + str(round(execution_time, 3)) + " segundos. Device: " + device + "\n")

def validate_device(is_local, device):
	""" Função que verifica se o device escolhido é valido

	Parâmetros:
		is_local(bool): Booleano que marca se a execução é local ou no backend da IBM
		device(str): Nome do device a ser utilizado

	Retorno:
		bool: Booleado que marca se é valido ou não o device escolhido
		
	"""
	valid_local_devices = [
							'aer_simulator',
							'aer_simulator_statevector',
							'aer_simulator_density_matrix',
							'qasm_simulator'
						]
	
	valid_remote_devices = [
							'simulator_mps',
							'ibmq_qasm_simulator',
							'ibmq_manila',
							'ibmq_bogota',
							'ibmq_santiago',
							'ibmq_quito',
							'ibmq_belem',
							'ibmq_lima',
							'ibmq_armonk'
						]

	if is_local:
		if device in valid_local_devices:
			return True
		else:
			return False
	else:
		if device in valid_remote_devices:
			return True
		else:
			return False

def test_from_pairs(pairs, shots, precision, is_local, device):
	""" Função que executa um teste com a partir de pares pré-definidos 

	Parâmetros:
		pairs([(int, int)]): Lista de pares que representam o sequente
		shots(int): Número de execuções do circuito em cada teste 
		precision(float): Numero entre 0 e 1 que marca a precisão mínima para que a
			execução seja considerada um sucesso
		is_local(bool): Booleano que marca se a execução é local ou no backend da IBM
		device(str): Nome do device a ser utilizado

	"""

	if validate_device(is_local, device) == False: 
		print("Device escolhido não é válido.")
		return

	is_single = False
	entries = len(pairs)

	f = open("test_results.txt", "a")

	start_time = time.time()

	result, answer = execute(entries, is_single, shots, precision, is_local, device, pairs)
	
	execution_time = time.time() - start_time

	log(is_single, device, entries, execution_time, shots, result, f, precision)

	return answer

