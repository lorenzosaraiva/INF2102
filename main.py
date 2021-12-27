from tests import tests, single_test

def test(is_single, device, qubits, is_local):
	""" Função que executa um teste com os parâmetro definidos

    Parâmetros:
    	is_single(bool): Booleano que marca se a execução é única ou completa
    	device(str): Nome do device a ser utilizado
    	qubits(int): Número de qubits no teste
    	is_local(bool): Booleano que marca se a execução é local ou no backend da IBM
 
    """
	single_test(is_single, device, qubits, is_local, 1000, 0.5)

def step_tests(start, end, shots, precision, is_local, device):
	""" Função que executa um conjunto de testes únicos com os parâmetros definidos

    Parâmetros:
    	start(int): Número de qubits da execução inicial
    	end(int): Número de qubits da execução final
		shots(int): Número de execuções em cada teste
		precision(float): Valor de 0 a 1 que marca a precisão mínima
			para um teste ser considerado de sucesso
		is_local(bool): Booleano que define se a execução é local
			ou no backend da IBM
		device(str): Nome do simulador ou computador quântico no qual
			o programa será executado
 
    """
	tests(start, end, shots, precision, 1, 0, 0, 0, is_local, simulator)

def complete_tests(start, end, shots, precision, is_local, device):
	""" Função que executa um conjunto de testes completos com os parâmetros definidos

    Parâmetros:
    	start(int): Número de qubits da execução inicial
    	end(int): Número de qubits da execução final
		shots(int): Número de execuções em cada teste
		precision(float): Valor de 0 a 1 que marca a precisão mínima
			para um teste ser considerado de sucesso
		is_local(bool): Booleano que define se a execução é local
			ou no backend da IBM
		device(str): Nome do simulador ou computador quântico no qual
			o programa será executado
 
    """
	tests(1, 0, 0, 0, start, end, shots, precision, is_local, simulator)

def full_tests(single_start, single_limit, single_shots, single_precision, complete_start, complete_limit, complete_shots, complete_precision, is_local, simulator):
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
		simulator(str): String com o nome do simulador utilizado

    """
	tests(single_start, single_limit, single_shots, single_precision, complete_start, complete_limit, complete_shots, complete_precision, is_local, simulator)


test(False, "simulator_mps", 3, False)