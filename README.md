# INF2102
INF2102 - PROJETO FINAL DE PROGRAMACAO


Especificação do programa
	
O programa é um algoritmo constrói um circuito quântico para realizar a verficação de uma prova em Lógica Linear multiplicativa de tensores. A partir de um sequente, o programa constrói uma database quântica entrelaçada que representa os pares de cláusulas atômicas, e depois utiliza o Grover Search Algorithm (GSA) para encontrar as divisões corretas na aplicação das regras do cálculo de sequentes. O programa foi implementado na linguagem Python e utiliza o framework open source de computação quântica da IBM, o Qiskit. A complexidade do algoritmo é de O(N log N), onde N é o número de pares de cláusulas atômicas na prova, que é melhor do que a complexidade do algoritmo clássico de O(2^N).


Projeto do Programa

O programa é composto pelos seguintes módulos:

- initialize.py - Módulo do Qiskit para inicializar estados quânticos arbitrários com algumas modificações. 
- encode.py - Módulo desenvolvido por  Araujo, I., Park, D., Petruccione, F. and da Silva, A.J. para o paper A divide-and-conquer algorithm for quantum state 		preparation que tem uma forma alternativa de inicializar estados quânticos arbitrários
- grover.py - Contém a parte principal, onde é feita a montagem e execução do circuito do Grover.  
- tests.py - Contém uma sequência automatizada dos testes 
- utils.py - Contém as funções auxiliares
- main.py - Módulo principal que será utilizado pelo usuário


O enconde.py e o initialize.py tem funções equivalentes - preparar um estado quântico arbitrário. O initialize.py tem uma complexidade teórica de O(2^n), onde n é o número de qubits, o que inviabilizaria o ganho teórico do algoritmo. O encode.py utiliza um método desenvolvido em 2021, com complexidade de O(n), que permite o algoritmo ter um ganho de complexidade. Entretanto, quando aplicados nos testes, o encode.py tem uma demora superior. Isso ainda esta sendo investigado, mas possíveis causas são a otimização do initialize.py por ser um módulo padrão do próprio Qiskit ou, já que a complexidade é assimptótica, é possível que o initialize.py tenha uma melhor performance em valores menores do que o encode.py 

Roteiro de testes:

Por ser um programa de computação quântica, os testes estão limitados pela questão de disponibilidade de computadores e/ou simuladores quânticos com um volume de qubits suficiente para testar o algoritmo completo para sequentes com mais de 4 cláusulas atômicas de cada lado. Por esse motivo, existem dois tipos de testes: os completos e os únicos. Tests únicos executam apenas um passo do algoritmo, e por isso não precisam das diversas cópias da base de dados entrelaçadas. Portanto, eles têm menos qubits, sendo possível testar se o passo teórico funciona para quantidades de qubits que não é possível testar o algoritmo completo. 

Além dos dois tipos de teste, existem 3 formas de testar: simular localmente, simular no backend da IBM e rodar em computadores quânticos reais da IBM. Cada uma dessas formas vêm com suas limitações:

- Locais: o número máximo de qubits simulável e a duração da simulação será determinado pela capacidade de memória RAM do computador. 
- Simuladores no backend da IBM: o número máximo de qubits será definido pelo simulador escolhido e a duração da simulação será determinado pela capacidade de memória RAM disponibilizada pela IBM. Também é possível que exista uma fila de espera para usar o simulador.
- Computadores Quânticos: o número máximo de qubits é definido pela propriedade do computador escolhido. É possível que exista uma fila de espera para usar o computador. A IBM só disponibiliza ao público em geral computadores de até 5 qubits, só sendo possível fazer os testes únicos com 1 passo executado.


Foram feitos os seguintes testes:

- Testes únicos de 4 a 32 pares, execução local no 'qasm_simulator'.
- Testes completos de 4 a 12 pares, execução no backend da IBM no 'simulator_mps'. 
- Testes únicos de 4 pares nos computadores quânticos da IBM.

Documentação para o Usuário:

Primero de tudo, é necessário instalar a linguagem Python (https://www.python.org/downloads/) e o framework de computação quântica Qiskit (https://qiskit.org/documentation/stable/0.24/install.html)
O usuário realiza os testes através do script exe.sh e modificando as variáveis no param.txt. As varíaveis do param.txt são as seguintes:

single_start(int): Quantidade de cláusulas atômicas no primeiro teste único
single_limit(int): Quantidade de cláusulas atômicas no último teste único
single_shots(int): Execuções do circuito quântico para cada teste único
single_precision(float[0-1]): Precísão mínima para que o test único seja considerada um sucesso
complete_start(int): Quantidade de cláusulas atômicas no primeiro teste completo
complete_limit(int): Quantidade de cláusulas atômicas no último teste completo
complete_shots(int): Execuções do circuito quântico para cada teste completo
complete_precision(float[0-1]): Precísão mínima para que o teste completo seja considerada um sucesso
is_local(bool): Booleano que marca se a execução é local ou no backend da IBM
device(str): String com o nome do simulador ou computador quântico utilizado utilizado

Caso se deseje executar apenas o único ou apenas o completo, basta colocar um limite menor que o começo que não serão executados testes daquele tipo. Os resultados serão acrescentados ao test_results.txt


Os devices disponíveis são:

- Locais:
	'aer_simulator',
	'aer_simulator_statevector',
	'aer_simulator_density_matrix',
	'qasm_simulator'

- Simuladores no backend da IBM:
	'simulator_mps',
	'ibmq_qasm_simulator'

- Computadores Quânticos (todos com apenas 5 qubits):
	'ibmq_manila',
	'ibmq_bogota',
	'ibmq_santiago',
	'ibmq_quito',
	'ibmq_belem',
	'ibmq_lima'
	


