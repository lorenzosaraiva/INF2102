from tests import tests, single_test

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
	f = open("param.txt", "r")
	single_start = int(f.readline())
	single_limit = int(f.readline())
	single_shots = int(f.readline())
	single_precision = float(f.readline())
	complete_start = int(f.readline())
	complete_limit = int(f.readline())
	complete_shots = int(f.readline())
	complete_precision = float(f.readline())
	is_local = f.readline()
	device = str(f.readline()).rstrip("\n")

	if is_local == "True":
		is_local = True
	else:
		is_local = False

	tests(single_start, single_limit, single_shots, single_precision, complete_start, complete_limit, complete_shots, complete_precision, is_local, device)
