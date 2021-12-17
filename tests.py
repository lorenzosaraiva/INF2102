# Código criado por Lorenzo Saraiva
# Módulo de testes

from complete import execute
from complete import grover_single
from complete import grover_complete
import time


# Testes singulares
# Aqui é testado o equivalente a um passo do algoritmo. 
# Esses testes existem para verificar se a implementação do Alsing funciona para maior número de qubits


limite = 10

# Loop que testa execução singular aumentando gradualmente o número de qubits
for atomics in range(2, limite):

	start_time = time.time()

	result = execute(atomics, True)
	
	execution_time = time.time() - start_time

	if result == False:
		print("Erro na execução única com " + str(atomics) + " qubits. Duração: " + str(execution_time))
	else:
		print(str(atomics) + " qubits -- OK. Duração: " + str(execution_time))

# Testes completos
# Aqui é testado o algoritmo completo 
# Esses testes são limitados pela disponibilidade de computadores quânticos e/ou memória RAM para simular

limite = 4

exit()
for atomics in range(2, limite):

	result = execute(i, False)




#

