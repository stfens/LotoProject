import requests as rq  # Request acessa o site e traz algumas informações dele
# BeautifulSoup lê o texto em HTML e separa informações dele
from bs4 import BeautifulSoup as bs
import json as js  # Json lê o resultado do request e separa em uma lista e dicionarios
import random
# import fechamento


class Loto:

    def __init__(self):
        self.respostaFinal = []
        self.respostaProvisoria = []
        self.listaResultados = []
        self.listaRepetidos = []
        self.fora = []
        self.ultimo = 0
        self.casas = [0]*26
        self.valoresLotofacil = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        self.moldura = [1, 2, 3, 4, 5, 6, 10,
                        11, 15, 16, 20, 21, 22, 23, 24, 25]
        self.miolo = [7, 8, 9, 12, 13, 14, 17, 18, 19]

    # Função que retorna os números repetidos do concurso que foi passado
    def pegarUltimosConcursos(self):
        # Requesita do site suas indormações
        requisicao2 = rq.get(
            "https://www.mazusoft.com.br/lotofacil/tabela-repetidas.php")
        last = self.obterUltimo()
        for i in range(last, last-11, -1):
            # Verifica se pode acessar o sites se sim extrai o dado e retorna TRUE
            if (requisicao2.status_code == 200):
                content = requisicao2.text  # Extrai o texto do site
                # Lê o texto do site com beautifulsoup e separa informações
                soup = bs(content, "html.parser")
                tabela = soup.select('table')  # Separa a tabela
                if (tabela):  # Se existir faz a separação
                    # Dentro da tabela, separa todas as tags TR que são as linhas da tabela
                    linhas = tabela[0].find_all("tr")
                    # tabela com 14 linhas, separamos nela os ultimos 10 concursos
                    resultados = linhas[2:13]
                    try:  # Tenta
                        for resultado in resultados:  # Roda a tabela linha a linha
                            # Pega a linha e extrai os dados TD contem "table data"
                            celulas = resultado.find_all('td')
                            # Se o concurso que foi passado for igual a posição 0 da linha da tabela que vai ser sempre o consurso ele entra dentro do IF
                            if (i == int(celulas[0].text.strip())):
                                # Separa posição 1 da linha que são as dezenas
                                dezenas = celulas[1].text.strip()
                                # Separa posição 2 da linha que são os números repetidos
                                repetidos = celulas[2].text.strip()
                                # separa o valor de numeros repetidos
                                num = celulas[3].text.strip()
                                dezenas = dezenas.split()
                                x = list(map(int, dezenas))
                                repetidos = repetidos.split()
                                y = list(map(int, repetidos))
                                z = self.naoCairam(x)
                                self.listaResultados.append(x+z)
                                self.listaRepetidos.append(
                                    {'repetidas': y, 'quantidadeRep': int(num)})
                    except:  # Se não der certo dá uma menssagem de erro
                        print("valor inexistente")
                else:
                    print("Tabela não encontrada")
                    return False
            else:  # se não mostra erro e retorna FAlSO
                print("Erro, sem permissão  para acessar o site")
                return False
    """ def retornaDezenas(concurso):#Busca concurso e separa os valores pertinentes para o programa
        try:
            requisicao=rq.get("https://loteriascaixa-api.herokuapp.com/api/lotofacil/"+str(concurso))# Pede para Api os valores do concurso pedido
            conteudo=js.loads(requisicao.content)# pega o resultado do site e separa em dicionarios e listas conforme o JSon
            dezenas=conteudo['dezenas']# Separa as dezenas vencedoras
            print(dezenas)
            return dezenas
        except:
            print("Error, concurso não encontrado") """

    def obterUltimo(self):
        # Pede para Api os valores do ultimo concurso
        requisicao = rq.get(
            "https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest")
        # pega o resultado do site e separa em dicionarios e listas conforme o JSon
        conteudo = js.loads(requisicao.content)
        concurso = conteudo['concurso']  # Separa as dezenas vencedoras
        self.ultimo = int(concurso)
        return int(concurso)

    def compararDezUltimosJogos(self, lista):
        maior = 0
        for i in range(len(lista)):
            casas = []
            for j in range(25):
                try:
                    if lista[i][j] == lista[i + 1][j]:
                        casas.append(str(j + 1))
                        self.casas[j + 1] += 1
                except:
                    pass
            if casas:
                print(
                    f"Nos jogos {self.ultimo - i} e {self.ultimo - (i + 1)}, as casas {' '.join(casas)} foram repetidas!")

    def escrever_na_ultima_linha(texto, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r') as arquivo:
                linhas = arquivo.readlines()

            with open(caminho_arquivo, 'a') as arquivo:
                if len(linhas) > 0:
                    # Adicionar uma nova linha antes do texto
                    arquivo.write('\n')

                arquivo.write(texto)
            print("Texto foi adicionado à última linha do arquivo com sucesso.")
        except IOError:
            print("Erro ao gravar o arquivo.")

    def naoCairam(self, lista):
        try:
            nCaiu = []
            for i in range(len(self.valoresLotofacil)):
                if (self.valoresLotofacil[i] not in lista):
                    nCaiu.append(int(self.valoresLotofacil[i]))
            return nCaiu
        except Exception as e:
            print("Erro", e)

    def naoRepetiram(self, lista):
        try:
            nrep = []
            for i in range(len(lista)):
                if (lista[i] not in self.listaRepetidos[1]["repetidas"]):
                    nrep.append(int(lista[i]))
            return nrep
        except Exception as e:
            print("Erro", e)

    def escolhaDeValores(self, repetidos, naoRep, naoCairam):
        parte1 = []
        parte2 = []
        parte3 = naoCairam
        try:
            while len(parte1) != 7:
                aleatorio = random.choice(repetidos)
                if (aleatorio not in parte1):
                    parte1.append(aleatorio)
            if (len(naoRep) > 4):
                while len(parte2) != 5:
                    aleatorio = random.choice(naoRep)
                    if (aleatorio not in parte2):
                        parte2.append(aleatorio)
                for _ in range(2):
                    aleatorio = random.choice(naoCairam)
                    indi = (parte3.index(aleatorio))
                    parte3.pop(indi)
                print("repetidos:", parte1, "naoRep:",
                      parte2, "naoCairam:", parte3)
                resposta = parte1+parte2+parte3
                resposta.sort()
                self.molduraMiolo(resposta)
            else:
                parte2 = naoRep
                resposta = parte1+parte2+parte3
                resposta.sort()
                self.molduraMiolo(resposta)

        except Exception as e:
            print("erro", e)

    def molduraMiolo(self, lista):
        try:
            par = 0
            impar = 0
            moldura = 0
            miolo = 0
            for i in lista:
                if (i in self.moldura):
                    moldura += 1
                    if ((i % 2) == 0):
                        par += 1
                    elif ((i % 2) == 1):
                        impar += 1
                elif (i in self.miolo):
                    miolo += 1
                    if ((i % 2) == 0):
                        par += 1
                    elif ((i % 2) == 1):
                        impar += 1
            if (miolo == 8 and moldura == 12):
                if (par == 10 and par == 10):
                    numeros_formatados = [str(numero).zfill(2)
                                          for numero in lista]
                    print("Aqui estão os 20 números:", *numeros_formatados)
                    return numeros_formatados
                else:
                    self.escolhaDeValores(loto.listaRepetidos[1]["repetidas"], naoRep[0:len(
                        naoRep)-10], loto.listaResultados[1][15:25])
            else:
                self.escolhaDeValores(loto.listaRepetidos[1]["repetidas"], naoRep[0:len(
                    naoRep)-10], loto.listaResultados[1][15:25])
        except Exception as e:
            print("erro:", e)


loto = Loto()
loto.pegarUltimosConcursos()
loto.compararDezUltimosJogos(loto.listaResultados)
naoCaiu = loto.naoCairam(loto.listaResultados[1])
naoRep = loto.naoRepetiram(loto.listaResultados[1])
print("Ultimo Resultado completo:", *(loto.listaResultados[1]))
print("Repetidas:", *(loto.listaRepetidos[1]["repetidas"]))
print("Não repetidas:", *(naoRep[0:len(naoRep)-10]))
print("Não cairam:", *(loto.listaResultados[1][15:25]))
sequencia = loto.escolhaDeValores(loto.listaRepetidos[1]["repetidas"], naoRep[0:len(
    naoRep)-10], loto.listaResultados[1][15:25])

# val=fechamento.gerar_fechamento(sequencia,14)
# print(val)
