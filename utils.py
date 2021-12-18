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