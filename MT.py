class mt: #Objeto da MT
    def __init__(self, estado, lendo, escreve, direcao = None,nvEstado = None, mostrar = None):
        self.estado     = estado
        self.lendo      = lendo
        self.escreve    = escreve
        self.direcao    = direcao
        self.nvEstado   = nvEstado
        self.mostrar    = mostrar

    def __str__(self):#forma que vai ser printado, acho q assim fica mais facil pra debugar vaso necessario
        return f"estado: {self.estado}\nlendo: {self.lendo}\nescreve: {self.escreve}\ndirecao: {self.direcao}\nnvEstado: {self.nvEstado}\nmostrar: {self.mostrar}"
    
    def estado(self):
        return str(self.estado)

    def lendo(self):
        return str(self.lendo)
    
    def escreve(self):
        return str(self.escreve)

    def direcao(self):
        return str(self.direcao)
    
    def nvEstado(self):
        return str(self.nvEstado)
    
    def nvEstado(self):
        return str(self.nvEstado)

    def mostrar(self):
        return str(self.mostrar)
    
buffer = list()

# numExe = 0

def lerArquivo(arq):#função para leitura do arquivo, e organizando no objeto mt
    arquivo = list()
    allComandos = list()
    comandos = list()

    #todos os programas devem etar na pasta 'programas' e devem seguir o modelo do t.txt
    with open('programas/'+arq,'r',encoding='utf-8') as arquivo:
        arquivo = arquivo.readlines()

    #lendo linha por linha e tirando os '\n'
    for linha in arquivo:
        if linha[0] == ';':
            pass
        else:
            allComandos.append(linha.replace('\n', '').split())

    # colocando as informações de cada linha no objeto
    for comando in allComandos:
        if 'bloco' in comando:
            comandos.append((comando[0],comando[1],comando[2]))
        elif 'fim' in comando:
            comandos.append(comando[0])
        elif len(comando) == 3:
            # <estado atual> <identificador de bloco> <estado de retorno>
            aux = mt(comando[0],comando[1],comando[2])
            comandos.append(aux)
        elif len(comando) == 5:

            aux = mt(comando[0],comando[1],comando[2],comando[3],comando[4])
            comandos.append(aux)
        elif len(comando) == 6:
            aux = mt(comando[0],comando[1],comando[2],comando[3],comando[4],comando[5])
            comandos.append(aux)
        else:
            continue

    return comandos

def geraFita(alfabeto):
    linhas = int((50-len(alfabeto))/2)
    fitaBase = ('_'*linhas) + alfabeto + (linhas*'_')

    return fitaBase

def primeiraPos(fitaBase):
    for i in range(0,len(fitaBase)):
        if fitaBase[i] != '_':
            pos = i
            break

    return pos


def cabecote(fita,pos):
    newFita = ''
    for i in range(0,pos):
        newFita = newFita+fita[i]
    
    newFita = newFita + '(' + fita[pos] + ')'

    for i in range(pos+1,len(fita)):
        newFita = newFita+fita[i]
    
    return newFita

def geraRegistro(bloco,estado):
    numPon = (16-len(bloco))
    tEstado = (4-len(estado))
    
    registro = '.' * numPon + bloco + ':' + '-' * tEstado + estado + ':'

    return registro

def alteraFitaBase(fita,pos,escrita):
    newFita = ''
    for i in range(0,pos):
        newFita = newFita+fita[i]
    
    newFita = newFita + escrita

    for i in range(pos+1,len(fita)):
        newFita = newFita+fita[i]

    return newFita
    

def executa(comandos,alfabeto,exe,numLinha = None,pos = None,estIni=None):
    fitaBase = geraFita(alfabeto)
    if pos == None:
        pos = primeiraPos(fitaBase)
    lendo = fitaBase[pos]
    fita = cabecote(fitaBase,pos)
    estado = ''
    fitaVirgem = True
    linha = 0
    print("Alfabeto: ",alfabeto)
    print("NumLinha: ",numLinha)
    quebra= False


    cont = 0
    while True:
        # print("Comeco")
        cont = 0
        for comando in comandos:
            # print(linha)
            # print(comando)
            # print('-'*10)
            
            if fitaVirgem:
                bloco = comando[1]
                estado = comando[2]
                registro = geraRegistro(bloco,estado)
                linha = linha + 1
                print(registro+fita)
                cont = cont+1
                # quebra = True

            elif(comando == 'fim'):
                if len(buffer) == 0:
                    break
                else:
                    nvAlfabeto = fitaBase.replace("_","")
                    return nvAlfabeto

            elif linha == numLinha:
                nvAlfabeto = fitaBase.replace("_","")
                # print(nvAlfabeto)
                while True:
                    exe = input("Digite a forma de execussão:\n\tr - Resume\n\tv - Verbose\n\ts - Step\n")

                    if exe in ['r','v','s']:
                        if exe == 's':
                            numLinha = int(input("Até qual linha? "))
                            executa(comandos,nvAlfabeto,exe,numLinha,pos)
                        else:
                            executa(comandos,nvAlfabeto,exe,None,pos)
                        # print('Execução Resume')
                        break
                    else:
                        print('Digete uma opção valida')
                        continue
                

            elif fitaVirgem == False and comando == comandos[0]:
                continue

            elif (comando.estado == estado) and (lendo == comando.lendo or comando.lendo == '*'):
                # if lendo == comando.lendo or comando.lendo == '*':

                if comando.escreve != '*':
                    fitaBase = alteraFitaBase(fitaBase,pos,comando.escreve)
                    quebra = True

                if comando.direcao != 'i':# Verifica se não é imovel
                    if comando.direcao == 'r' or comando.direcao == 'd':
                        pos = pos+1
                        fita = cabecote(fitaBase,pos)
                    elif comando.direcao == 'l' or comando.direcao == 'e':
                        pos = pos-1
                        fita = cabecote(fitaBase,pos)
                
                # print(registro+fita)
                if comando.nvEstado == 'halt-accept': 
                    print("Aceito: ")
                    linha = linha + 1
                    registro = geraRegistro(bloco,estado)
                    fitaBase = alteraFitaBase(fitaBase,pos,comando.escreve)
                    print(registro+fitaBase)
                    # print(comando.estado)
                    print("Fim")
                    nvAlfabeto = fitaBase.replace("_","")
                    return nvAlfabeto
                
                elif(comando.nvEstado == 'halt-reject'):
                    print("Erro: ")
                    registro = geraRegistro(bloco,estado)
                    fitaBase = alteraFitaBase(fitaBase,pos,comando.escreve)
                    print(registro+fita)
                    # print(comando.estado)
                    print("Fim")
                    return
                estado = comando.nvEstado
                lendo = fitaBase[pos]
                # print(estado+'/'+lendo)
                linha = linha + 1
                if exe == 'v' or comando.mostrar == "!":
                    registro = geraRegistro(bloco,estado)
                    print(registro+fita)
                    # quebra = True
                elif comando.direcao == None and comando.nvEstado == None:
                    print("Entrei :D")
                    dados = {"bloco": comandos[0][1], "retorno": comando.escreve}
                    buffer.append(dados)
                    
                    nvAlfabeto = fitaBase.replace("_","")
                    
                    arquivo = comando.lendo + '.txt'
                    nvComandos = lerArquivo(arquivo)
                    
                    nvAlfabeto = executa(nvComandos,nvAlfabeto,'v',None,pos)
                   
                    estado = buffer[-1]["retorno"]
                    buffer.pop()
                    
                else:
                    continue

            else:
                continue

            cont = cont +1
            fitaVirgem = False
            if quebra:
                break


if __name__== "__main__":
    arq = input("Diga o nome do arquivo (com .txt no final): ")

    comandos = lerArquivo(arq)

    alfabeto = input("Digite o alfabeto: ")
    while True:
        exe = input("Digite a forma de execussão:\n\tr - Resume\n\tv - Verbose\n\ts - Step\n")

        if exe in ['r','v','s']:
            if exe == 's':
                numLinha = int(input("Até qual linha? "))
                executa(comandos,alfabeto,exe,numLinha)
            else:
                executa(comandos,alfabeto,exe)
            # print('Execução Resume')
            break
        else:
            print('Digete uma opção valida')
            continue