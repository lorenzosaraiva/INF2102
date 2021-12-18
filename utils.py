###############  Módulo auxiliar ############### 


def to_bin (x, n = 0):
	"""Função  para converter números decimais para binário
	
	Parâmetros:
		x(int): Número a ser convertido
		n(int): Número de dígitos a serem utilizados
	
	Retorno:
		Número 'x' convertido para binário utilizando 'n' dígitos
	"""
	return format(x, 'b').zfill(n)


def reverse(x):
	"""Função para inverter lista
	
	Parâmetros:
		x(list):lista a ser invertida
	  
	
	Retorno:
		lista 'x' invertida
	"""
	return x[::-1]


def binaryToDecimal(n):
	"""Função para converter números binários para decimal
	
	Parâmetros:
		n(binário): Número a ser convertido
	  
	
	Retorno:
		Número 'n' convertido para decimal
	"""
	return int(n,2)

