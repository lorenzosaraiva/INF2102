import numpy as np
import math
import random
from initialize import Initialize

from qiskit import IBMQ, Aer, assemble, transpile
from qiskit.providers.aer import AerSimulator
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq import least_busy
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary as sel
from qiskit.transpiler.passes import BasisTranslator
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.circuit.library import MCMT


###############  Funções auxiliares ############### 


# Função auxiliar para converter números decimais para binário
# Input:
#   x - número a ser convertido
#   n - número de dígitos a serem utilizados

# Output:
#   número convertido para binário na quantidade informada de dígitos

def to_bin (x, n = 0):
    return format(x, 'b').zfill(n)


# Função auxiliar para inverter array
# Input:
#   x - array a ser invertido

# Output:
#   array invertido

def reverse(x):
  return x[::-1]


# Função auxiliar para converter números binários para decimal
# Input:
#   n - número a ser convertido

# Output:
#   número convertido para decimal

def binaryToDecimal(n):
    return int(n,2)

############### Fim funções auxiliares ######################

###############  Funções relativas ao circuito quântico  ############### 

# Função que constrói um oráculo dinamicamente para a iteração do Grover
# Input:
#   qc - Circuito quântico que será modificado
#   var - Qubits sobre os quais será feito o oráculo
#   output_qubit - Qubit utilizado para o phase kickback
#   target - Valor a ser procurado pelo oráculo
#   n - número de qubits em var

def generic_oracle(qc, var, output_qubit, target, n):

    binary = reverse(to_bin(target, n))

    # Onde tem zeros, faz o Pauli-X
    for i in range(n):
        if binary[i] == '0':
            qc.x(var[i])

    # Marca a solução
    qc.mct(var, output_qubit)


    # Desfaz as mudanças
    for i in range(n):
        if binary[i] == '0':
            qc.x(var[i])

# Função que constrói um difusor  para a iteração do Grover
# Input:
#   qc - Circuito quântico que será modificado
#   n - Número de qubits 
#   qubits - Qubits que serão afetados pelo difusor
#   uncompute - Sequência de gates para a transformação |s> -> |00..0> 
#   prepare - Sequência de gates para a transformação |00..0> -> |s>
#   v - Índice da variável que está sendo buscada

def diffuser(qc, n, qubits, uncompute, prepare, v):
    

    size = n * 2
    start = v * size
    
    # Aplica transformação |s> -> |00..0> 
    qc.append(uncompute, qubits[start: start + size])

    # Aplica transformação |00..0> -> |11..1> 
    qc.x(qubits[start: start + size])

    # Aplica um multi-controlled Z 
    qc.h(qubits[start + size - 1])
    qc.mct(list(range(start, start + size - 1)), start + size - 1)  # multi-controlled-toffoli
    qc.h(qubits[start + size - 1])

    
    # Aplica transformação |11..1> -> |00..0>
    qc.x(qubits[start: start + size])

    qc.barrier()

    # Aplica transformação |00..0> -> |s>
    qc.append(prepare, qubits[start: start + size])

def groover(n, entries, uncompute, prepare):
    # Cria os registros

    size = n * 2
    var_qubits = QuantumRegister((size) * entries, name='v') # Define o registrador quântico que representa as variáveis
    output_qubit = QuantumRegister(1, name='out') # Define um qubit para o phase kickback
    c_bits = ClassicalRegister(n * entries, name='c') # Define um registrador clássico para ser feita a medição


    qc = QuantumCircuit(var_qubits, output_qubit, c_bits)  # Cria o circuito quântico

    
    # Prepara o estado quântico correto em N grupos de 2n qubits
    for i in range(entries):   
        qc.append(prepare, var_qubits[i * entries: i * entries + size]) 
        

    qc.initialize([1, -1]/np.sqrt(2), output_qubit) # Prepara o qubit de phase kickback no estado correto


    num_iterations = math.floor(((math.pi) * math.sqrt(entries))/4) # Calcula o numero ótimo de iterações do GSA
    

    # Loop do GSA

    for v in range(entries): 
        for i in range(num_iterations):
            generic_oracle(qc, var_qubits[v * size: v * size + n], output_qubit, v, n)  # Aplica Oracle oráculo nos qubits de busca
                      
            qc.barrier() 

            diffuser(qc, n, var_qubits, uncompute, prepare, v)  # Aplica o difusor

        
            qc.measure(var_qubits[v * size + n:v * size + 2 * n], c_bits[v * n:v * n + n]) # Faz a medições
            qc.barrier()

    

    qc.barrier()

    # Simulação do circuito
    qasm_simulator = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, qasm_simulator)
    qobj = assemble(transpiled_qc)
    result = qasm_simulator.run(qobj, shots = 1000).result() # Circuito simulado 1000 vezes

    # Coleta e imprime os resultados e o circuito
    d = dict(sorted(result.get_counts().items(), key=lambda item: item[1]))
    print(qc)
    print(d)

#QuantumCircuit.initialize = initialize


n = 2 # Numero de qubits pra cada parte
entries = 2 ** n # numero de pares 
ceil = entries ** 2 # valor máximo 

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
    indexes.append(pairs[i][0] * entries + pairs[i][1])

# Prepara o vetor de estados de acordo com os índices calculados
initial_state = [0] * ceil

for i in range(entries):
    initial_state[indexes[i]] = math.sqrt(1/entries)

# Cria conjunto de gates |s> -> |00..0>  e |00..0> -> |s>
init_instruction = Initialize(initial_state)

inverse_init_gate = init_instruction.gates_to_uncompute()

init_gate = inverse_init_gate.inverse()


groover(n, entries, inverse_init_gate, init_gate)
