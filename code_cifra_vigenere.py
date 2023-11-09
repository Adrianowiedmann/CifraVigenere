#Alunos:
# Adriano Ulrich do Prado Wiedmann - 202014824 (Turma 1);
# Vinícius Giovani Moreira Nascimento - 170115437 (Turma 2).


from collections import Counter
import math
import os

#FREQUENCIA NA LÍNGUAS PORTUGUESA
freq_portuguesa = {'A': 0.1463, 'B': 0.0104, 'C': 0.0388, 'D': 0.0499, 'E': 0.1257,
             'F': 0.0102, 'G': 0.0130, 'H': 0.0128, 'I': 0.0618, 'J': 0.0040,
             'K': 0.000, 'L': 0.0278, 'M': 0.0474, 'N': 0.0505, 'O': 0.1073,
             'P': 0.0252, 'Q': 0.012, 'R': 0.0653, 'S': 0.0781, 'T': 0.0434,
             'U': 0.0463, 'V': 0.0167, 'W': 0.0001, 'X': 0.0021, 'Y': 0.0001, 'Z': 0.0047}

freq_ingles = {'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228, 'G': 0.02015, 
               'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 
               'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056, 'U': 0.02758, 
               'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 'Z': 0.00074}

#Seleciona o idioma
def idioma(op):
    if op == 1:
        return freq_portuguesa
    else:
        return freq_ingles

#Através da key, obtem a keystream
def get_keystream(k, p):
    k_flag = k.copy()
    i=0
    while len(k)<len(p):
        k.append(k_flag[i])
        i+=1
        if i>=len(k_flag):
            i=0
    return k

#Cifra plaintext de acordo com a keystream
def get_ciphertext(k,p):
    ciphertext = ""
    for i,j in zip(k,p):
        soma = (ord(i)-65)+(ord(j)-65)
        soma = (soma%26)+65
        ciphertext =  ciphertext + chr(soma)
    return ciphertext

#Decifra usando o criptograma (ciphertext) e a senha (keystream)
def get_deciphertext(c,k):
    deciphertext = ""
    for i,j in zip(c,k):
        if ord(j)>ord(i):
            soma = 26-(ord(j)-ord(i))+65
        else:
            soma = ord(i)-ord(j)+65
        deciphertext = deciphertext + chr(soma)
    return deciphertext

def distancia_trigramas(text, list_tri):
    dict_trigramas = dict()
    for tri in list_tri:
        dict_trigramas[tri] = []
        posicao = text.find(tri)
        while posicao != -1:
            dict_trigramas[tri].append(posicao)
            posicao = text.find(tri, posicao+1)
     
    distancias = dict()
    for tri in list_tri:
        distancias[tri] = []
        for i in range (len(dict_trigramas[tri])-1):
            distancias[tri].append(dict_trigramas[tri][i+1]-dict_trigramas[tri][i])
    
    return distancias
   
def tamanho_chave(text, m_lenght):
    list_tri = []
    i=3
    for i in range(len(text) - i):
        trigrama = text[i:i+3]
        if trigrama not in list_tri:
            if text.count(trigrama) > 1:
                list_tri.append(trigrama)
        i+=1
    dist_trigrama = distancia_trigramas(text, list_tri)
    trigramas_ordenado = dict(sorted(dist_trigrama.items(), key=lambda x: len(x[1]), reverse=True))
    
    lista_completa = []

    #Junta todas as lista do dicionario dist_trigrama
    for chave in dist_trigrama:
        lista_completa.extend(dist_trigrama[chave])
    
    lista = []
    i=3
    while i < (m_lenght+1):
        qtd=0
        for j in range(len(lista_completa)):
            if lista_completa[j]%i==0:
                qtd+=1
        lista.append([i,qtd])
        i+=1
    tam_chave = None; maior_valor = None
    for x in lista:
        if tam_chave is None or x[1] > maior_valor:
            tam_chave, maior_valor = x[0], x[1]
    return tam_chave


def encontrar_letra(segs, frequencia):
    #conta a frequencia de cada letra
    freq_counts = [Counter(s) for s in segs]
    
    # calcula a frequencia esperada
    expected_freq = {chr(ord(i)): freq/len(segs) for i, freq in frequencia.items()}
    
    list_freq = []
    for x in range(26):
        total = 0
        for freq in freq_counts:
            x_freq = {chr((ord(c) - 65 - x) % 26 + 65): count for c, count in freq.items()}
            total += sum(((x_freq.get(c, 0)/len(segs)) - expected_freq[c])**2/expected_freq[c] for c in expected_freq)
        list_freq.append(total)
    
    return chr(list_freq.index(min(list_freq)) + 65)


def descobrir_chave(texto, tam_chave, op):
    segmentos = dividir_cifra(texto, tam_chave)
    frequencia = idioma(op)
    chave = ""
    for i in range(tam_chave):
        segmentos2 = [sublista[i] for sublista in segmentos if len(sublista) > i and len(sublista[i]) > 0]
        #segmentos2 = [sublista[i] for sublista in segmentos if len(sublista) > 0]
        chave+=encontrar_letra(segmentos2, frequencia)
    return chave


def dividir_cifra(texto, tam_chave):
    segmentos = []
    for i in range(0, len(texto), tam_chave):
        segmento = texto[i:i+tam_chave]
        segmentos.append(segmento)
    return segmentos

def limpar_string(string):
    letras = []
    for letra in string:
        if letra.isalpha():
            letras.append(letra.upper())
    return ''.join(letras)
    
def ler_txt(chose):
    if(chose == "1"):
        with open('desafio1.txt', 'r', encoding='utf-8') as file:
            content = file.read()
    elif(chose == "2"):
        with open('desafio2.txt', 'r', encoding='utf-8') as file:
            content = file.read()
    elif(chose == "3"):
        with open('cypher3.txt', 'r', encoding='utf-8') as file:
            content = file.read()
    else:
        print("Opcao invalida! Escolhendo a opção 3...")
        with open('cypher3.txt', 'r', encoding='utf-8') as file:
            content = file.read()
    filtered_content = ''.join(filter(str.isalpha, content))
    return filtered_content.upper()


if __name__ == '__main__':
    while(1):
        print("###################### CRIPTOGRAFIA ######################")
        print("#################### CIFRA DE VIGENERE ####################")
        print("###########################################################")

        print("Para aumentar o nível de segurança, as palavras são compostas de 5 letras...")
        print("...e as letras mortas do criptograma serão ASFW")

        print("Escolha uma opcao: ")
        print("1 - Criptografar")
        print("2 - Descriptografar")
        print("3 - Quebrar um criptograma")
        print("4 - Sair")

        #mortas = "ASFW"
        #mortas = list(mortas)
        max_lenght = 20
        
        opcao = input("Opcao: ")
        if(opcao == "1"):
            plaintext = input("Insira a mensagem a ser codificada: ")
            plaintext = limpar_string(plaintext)
            plaintext = list(plaintext)
   
            key = input("Insira a chave: ")
            key = key.upper()
            key = list(key)
            keystream = get_keystream(key,plaintext)
            ciphertext = get_ciphertext(keystream,plaintext)
            print("\n\nMensagem criptografada: ")
            print(ciphertext)
            input()

        elif(opcao == "2"):
            ciphertext = input("Insira a mensagem a ser decodificada: ")
            ciphertext = limpar_string(ciphertext)
            ciphertext = list(ciphertext)
            key = input("Insira a chave necessaria: ")
            key = key.upper()
            key = list(key)
            keystream = get_keystream(key,ciphertext)
            deciphertext = get_deciphertext(ciphertext,keystream)
            print(deciphertext)
            input()

        elif(opcao == "3"):
            print("\n1 - Portugues")
            opcao_idioma = input("2 - Ingles\nEscolha o idioma: ")
            print("\nopcao escolhida: ", opcao)
            print("Escolha o criptograma: ")
            print("1 - Desafio 1 (PT)")
            print("2 - Desafio 2 (EN)")
            print("3 - Criptograma 3")#Criptograma 3 criado pelo grupo
            chose = input("Opcao: ")
            ciphertext = ler_txt(chose)
            ciphertext = limpar_string(ciphertext)
            print("\nopcao escolhida: ", chose)
            
            key_lenght = tamanho_chave(ciphertext, max_lenght)
            chave = descobrir_chave(ciphertext, key_lenght, opcao_idioma)
            print(chave)
            input()
        elif(opcao == "4"):
            print("Saindo...")
            break