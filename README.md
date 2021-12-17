# INF2102
INF2102 - PROJETO FINAL DE PROGRAMACAO


Especificação do programa

O programa é um algoritmo constrói um circuito quântico para realizar a verficação de uma prova em Lógica Linear multiplicativa de tensores. A partir de um sequente, o programa constrói uma database quântica entrelaçada que representa os pares de cláusulas atômicas, e depois utiliza o Grover Search Algorithm (GSA) para encontrar as divisões corretas na aplicação das regras do cálculo de sequentes. O programa foi implementado na linguagem Python e utiliza o framework open source de computação quântica da IBM, o Qiskit.


Projeto do Programa

O programa é composto pelos seguintes módulos:

- initialize.py - O initialize.py é um módulo do Qiskit para inicializar estados quânticos arbitrários com algumas modificações. 
- main.py - O main.py contém a parte principal, onde é feita a montagem e execução do circuito.  
- tests.py - O tests.py contém uma sequência automatizada dos testes 

Roteiro de Teste:

Por ser um programa de computação quântica, os testes estão limitados pela questão de disponibilidade de computadores e/ou simuladores quânticos com um volume de qubits suficiente para testar o algoritmo completo para sequentes com mais de 4 cláusulas atômicas de cada lado. Os testes realizados foram:



