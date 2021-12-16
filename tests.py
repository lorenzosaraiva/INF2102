# Código criado por Lorenzo Saraiva
# Módulo de testes

from complete import execute


# Testes singulares
# Aqui é testado o equivalente a um passo do algoritmo. 
# Esses testes existem para verificar se a implementação do Alsing funciona para maior número de qubits


limite = 10

# 
for atomics in range(2, limite):

	result = execute(i, True)

# Testes completos
# Aqui é testado o algoritmo completo 
# Esses testes são limitados pela disponibilidade de computadores quânticos e/ou memória RAM para simular

limite = 4


for atomics in range(2, limite):

	result = execute(i, False)