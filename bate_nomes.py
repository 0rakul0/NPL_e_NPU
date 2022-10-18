import re
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import openpyxl
import time

class bate_lista_nomes():
    def __init__(self):
        self.nome = ''
        self.lista_nomes = []
        self.lista_empresa = []

    def inicia(self):
        planilha = pd.read_excel('./dados/Primeiro_Nome.xlsx')
        for id, x in planilha.iterrows():
            try:
                nome_pesquisa = x['Nome pessoa fisica']
                self.nome = nome_pesquisa
                self.bate_nome(nome=nome_pesquisa)
                print(f"##############{id}###############")
            except:
                print(x['Nome pessoa fisica'])
        self.imprimir()

    def bate_nome(self, nome):
        op = Options()
        # op.add_argument('--headless')
        op.add_argument('--window-size=40,80')
        driver = webdriver.Chrome(executable_path='./chrome/chromedriver.exe', options=op)
        url = f"https://www.jusbrasil.com.br/busca?q={nome}"
        driver.get(url)
        soup = bs(driver.page_source, "html.parser")
        self.pesquisa(soup)
        driver.quit()

    def pesquisa(self, soup):

        passe = soup.find('div', {'class':'SnippetSlider-block scrollbar--hidden'})

        empresa_juridica = re.compile(
            'S\.A|S\/A|viacao|Construtora|Auto|Pecas|Peças|Estojos|Embalagens|Comercio|comércio|Laboratório|Imoveis|Sociedade|Incorporadora|Ltda\s?-\s?Me|Epp|Manutenc.o|Manutenç.o|CIA|Turismo|Industriais|Ltda|Admin|Adm|Administradora|Servicos|Serviços|Promotoria|Delegacia|Imobili.ria|Televis.o|Esporte',
            re.IGNORECASE)
        locais = re.compile('Município|Municipio|Promotoria|Delegacia')
        pessoa_fisica = re.compile(self.nome, re.IGNORECASE)

        passe_ml = passe.find_all('span', {'class':'SearchFeaturedLawsuit-snippet-title-anchor'})

        for x in passe_ml:
            x = x.text
            empresa = empresa_juridica.search(x)
            local = locais.search(x)
            if empresa is not None and local is None:
                self.lista_empresa.append(x)
                print('é empresa:>>',x)

            if local is None and empresa is None:
                pessoa = pessoa_fisica.search(x)
                if pessoa != None:
                    self.lista_nomes.append(x)
                    # print('é uma pessoa:>>',x)

    def imprimir(self):
        for nome in self.lista_nomes:
            print(nome)
        for empresas in self.lista_empresa:
            print(empresas)

if __name__ == "__main__":
    bt = bate_lista_nomes()
    bt.inicia()
