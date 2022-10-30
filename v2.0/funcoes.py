def complemento(n,tamanho):
    comp = n ^ ((1 << tamanho) - 1)
    return '0b{0:0{1}b}'.format(comp, tamanho)

def checksum(portaorigem, portadestino, comprimento):
    primeirasoma = bin(portaorigem+portadestino)[2:].zfill(16)
    if (len(primeirasoma)>16):
            primeirasoma = primeirasoma[1:17]
            primeirasoma = bin(int(primeirasoma,2) + 1)[2:].zfill(16)
    segundasoma = bin(int(primeirasoma,2)+comprimento)[2:].zfill(16)
    if (len(segundasoma)>16):
            segundasoma = segundasoma[1:17]
            segundasoma = bin(int(segundasoma,2) + 1)[2:].zfill(16)
    checksum = complemento(int(segundasoma,2),16)[2:]
    return int(checksum,2)