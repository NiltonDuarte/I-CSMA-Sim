#decodificador.py

"""da mesma forma que a mudanca de base foi feita para representar as combinacoes de binarios usando inteiros,
tambem eh possivel utilizar uma lista de numeros para representar um numero em base 2^64,
onde a ultima posicao na lista representaria a 'unidade', a penultima a 'dezena' da base 10 mas em base 2^64

"""

def decodificador(listaB, I, C):
	Q=listaB[-1]/2
	R=listaB[-1]%2
	listaB[-1] = Q
	#print R
	if (R==1):
		C = C + [I]
	if (Q>0):
		I = I + 1
		C = decodificador(listaB,I,C)
	else:
		#if there still a int in the B list
		if len(listaB)>1:
			I = ((I/64)+1)*64
			#remove last element
			listaB = listaB[:-1]
			C = decodificador(listaB,I,C)
	return C


listaB = [2**63+2**15,2**63+2**56+2**10,2**63+0xffff]
print "{0:b} \n{1:b} \n{2:b} \n".format(listaB[0],listaB[1],listaB[2])
"""listaB
"algarismo centena" = 2**63+2**15          = 1000000000000000000000000000000000000000000000001000000000000000
"algarismo da dezena"  = 2**63+2**56+2**10 = 1000000100000000000000000000000000000000000000000000010000000000
"algarismo da unidade" = 2**63+0xffff      = 1000000000000000000000000000000000000000000000001111111111111111

"""
C = []
I=0
print decodificador(listaB,I,C)

"""
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 63, 74, 120, 127, 143, 191]
zero até 15 são os 16 bits de 0xffff
63 eh o 2**63 da "unidade
74 = 64+10 eh o 2**10 da "dezena"
120 = 64+54 é o 2**56 da "dezena"
127 = 64+63 é o 2**63 da "dezena"
143 = 64+64+15 é o 2**15 da "centena"
191 = 64+64+63 é o 2**63 da "centena"
"""
