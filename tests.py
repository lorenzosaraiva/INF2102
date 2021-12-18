# Código criado por Lorenzo Saraiva
# Módulo de testes

from grover import grover_single
from grover import grover_complete
from utils import to_bin
from operator import itemgetter


import time
import random
import math

def execute(n, is_single):

	entries = 2 ** n # numero de pares

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

	print(pairs)

	# Calcula o índice de cada par no vetor de estado
	indexes = []

	for i in range(entries):
		indexes.append(pairs[i][0] * power + pairs[i][1])

	# Prepara o vetor de estados de acordo com os índices calculados
	initial_state = [0] * ceil

	for i in range(entries):
		initial_state[indexes[i]] = math.sqrt(1/entries)



	answer_dict = ""
	shots = 1000

	if is_single:

		target = random.randint(0, entries - 1)

		answer_dict = grover_single(n, entries, initial_state, target, shots)

		answer = compute_answer(answer_dict, pairs, is_single, target, n)

		# Pega o resultado mais frequente e sua frequência
		top_result = list(answer_dict.keys())[-1]
		accuracy = list(answer_dict.values())[-1]/shots

		threshold = 0.5


		print("Testes:")
		print(top_result)
		print(target)
		print(answer)
		print(accuracy)

		if top_result == answer and accuracy > threshold:
			return True
		else:
			return False
	else:

		answer_dict = grover_complete(n, entries, initial_state)

		answer = compute_answer(answer_dict, pairs, is_single, 0, n)
		

		print(answer)

		# Pega o resultado mais frequente e sua frequência
		top_result = list(answer_dict.keys())[-1]
		accuracy = list(answer_dict.values())[-1]/shots

		threshold = 0.5

		# caso o resultado esteja correto e a frequência seja maior que o limite, retorna True
		# caso contrário, retorna False


		print("Testes:")
		print(top_result)
		print(accuracy)

		if top_result == answer and accuracy > threshold:
			return True
		else:
			return False 

def compute_answer(answer_dict, pairs, is_single, target, n):  	

	if is_single:
		# Verifica qual era a resposta correta
		answer = -1

		for i in range(len(pairs)):
			pair = pairs[i]
			if pair[1] == target:
				answer = pair[0]

		return to_bin(answer, n)

	else:
		# Calcula a resposta correta
		pairs = sorted(pairs, key=itemgetter(1))
		pairs.reverse()
		answer = ""

		for pair in pairs: 
			answer = answer + str(to_bin(pair[0], n))

		return answer



# Testes singulares
# Aqui é testado o equivalente a um passo do algoritmo. 
# Esses testes existem para verificar se a implementação do Alsing funciona para maior número de qubits


limite = 5

# Loop que testa execução singular aumentando gradualmente o número de qubits
for atomics in range(2, limite):

	start_time = time.time()

	result = execute(atomics, False)
	
	execution_time = time.time() - start_time

	if result == False:
		print("Erro na execução única com " + str(atomics) + " qubits. Duração: " + str(execution_time))
	else:
		print(str(atomics) + " qubits -- OK. Duração: " + str(execution_time))
	break
# Testes completos
# Aqui é testado o algoritmo completo 
# Esses testes são limitados pela disponibilidade de computadores quânticos e/ou memória RAM para simular

# limite = 4

# for atomics in range(2, limite):

# 	result = execute(i, False)