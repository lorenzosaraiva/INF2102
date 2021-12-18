# Código criado por Lorenzo Saraiva
###############  Módulo de testes  ############### 

from grover import grover_search_algorithm

from utils import to_bin
from operator import itemgetter

import time
import random
import math

def execute(n, is_single, shots, threshold):
	"""Função que gera aleatoriamente um conjunto de pares e executa o Grover
    
    Parâmetros:
        n (int): Número de qubits em um lado da base de dados entrelaçada
        is_single(bool): Booleano que marca se é uma execução única ou completa
        shots(int): Número de execuções do circuito
        threshold(float): Valor de 0 a 1 que representa o valor de precisão mínima
        	para que a execução seja considerada de sucesso
 	
 	Retorno:
 		bool: Booleano relativo ao sucesso da execução
    """

	entries = 2 ** n # numero de pares

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

	# Cria os pares aleatórios
	pairs = []
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

	answer_dict = grover_search_algorithm(n, entries, initial_state, variables, target, shots)

	answer = compute_answer(answer_dict, pairs, is_single, target, n)

	# Pega o resultado mais frequente e sua frequência
	top_result = list(answer_dict.keys())[-1]
	accuracy = list(answer_dict.values())[-1]/shots

	print("Testes:")
	print(top_result)
	print(target)
	print(answer)
	print(accuracy)

	if top_result == answer and accuracy > threshold:
		return accuracy
	else:
		return 0

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

def test(single_limit, single_shots, single_precision, complete_limit, complete_shots, complete_precision):
	""" Função que executa conjunto de testes para execução única e execução completa
		de 2 cláusulas atômicas até o limite informado e gera um log com os resultados

    Parâmetros:
    	single_limit(int): Número de claúsulas atômicas máximo para a execução única
    	single_shots(int): Número de execuções do circuito em cada teste para a execução única
        single_precision(int): Precisão mínima para que uma execução única seja considerada um sucesso
        complete_limit(int): Número de claúsulas atômicas máximo para a execução completa
        complete_shots(int): Número de execuções do circuito em cada teste para a execução completa
 		complete_precision(int): Precisão mínima para que uma execução completa seja considerada um sucesso

    """

	f = open("test_results.txt", "w")

	# Testes únicos
	# Aqui é testado um único passo do algoritmo, portanto podem ser feitos testes com mais qubits
	# Loop que testa execução singular aumentando gradualmente o número de qubits
	for atomics in range(2, single_limit + 1):

		start_time = time.time()

		result = execute(atomics, True, single_shots, single_precision)
		
		execution_time = time.time() - start_time

		if result == 0:
			f.write("Erro na execução única com " + str(atomics) + " qubits. Duração: " + str(execution_time) + "\n")
		else:
			f.write(str(atomics) + " qubits única -- OK. Precisão: " + str(result) + " Duração: " + str(execution_time) + "\n")
		
	
	
	# Testes completos
	# Aqui é testado o algoritmo completo 
	# Esses testes são limitados pela disponibilidade de computadores quânticos e/ou memória RAM para simular
	for atomics in range(2, complete_limit + 1):

		start_time = time.time()
		
		result = execute(atomics, False, complete_shots, complete_precision)
		
		execution_time = time.time() - start_time

		if result == 0:
			f.write("Erro na execução completa com " + str(atomics) + " qubits. Duração: " + str(execution_time) + "\n")
		else:
			f.write(str(atomics) + " qubits completa -- OK. Precisão: " + str(result) + " Duração: " + str(execution_time) + "\n")
			


test(4, 1000, 0.5, 2, 1000, 0.5)