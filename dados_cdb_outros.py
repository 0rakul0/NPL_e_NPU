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



class bate_lista_cdb_outros():
    def __init__(self):
        self.nome = []

    def inicio(self, page, months):
        op = Options()
        op.add_argument('--headless')
        # op.add_argument('--window-size=640,480')
        driver = webdriver.Chrome(executable_path='./chrome/chromedriver.exe', options=op)
        url = f"https://yubb.com.br/investimentos/renda-fixa?collection_page={page}&investment_type=renda-fixa&months={months}&principal=5000.0&sort_by=net_return"
        driver.get(url)
        soup = bs(driver.page_source, "html.parser")
        #captura_dados
        dict_dados = self.extrator(soup)
        #salva_dados
        self.salva_dados(dict_dados, page)
        driver.quit()

    #salva os dados
    def salva_dados(self, dict_dados, pagina):
        print(pagina)
        df = pd.DataFrame(dict_dados)
        df.to_csv(f"./dados/6 meses/{pagina}__todos_6.csv", encoding='utf-8')


    #extrai dados
    def extrator(self, soup):
        bloco_informacoes = soup.find('div', {'class':'investmentCardContainer__body'})
        cards = bloco_informacoes.find_all('article', {'data-spec':'investments/card'})
        list_resultado_retorno = []
        list_resultado_rentabilidade = []
        list_resultado_empresa = []
        list_resultado_tag = []
        list_resultado_tipo = []
        list_resultado_rentabilidade_ano = []
        list_resultado_prazo = []
        list_resultado_distribuidor = []
        list_resultado_emissor = []

        for  card in cards:
            info_head = card.find('header',{'class':'stack'})
            #retorno
            try:
                resultado_retorno = info_head.find('div', {'class':'results__netReturn'})
                resultado_retorno = resultado_retorno.find('span', {'class':'sugarish__whole'}).text
                resultado_retorno = resultado_retorno.replace(',', '.')
            except:
                resultado_retorno = None
            list_resultado_retorno.append(resultado_retorno)
            #rentabilidade
            try:
                resultado_rentabilidade = info_head.find('div', {'class':'results__grossYield'})
                resultado_rentabilidade = resultado_rentabilidade.find('span',{'class':'sugarish__number'}).text
                resultado_rentabilidade = resultado_rentabilidade.replace(',', '.')
            except:
                resultado_rentabilidade = None
            list_resultado_rentabilidade.append(resultado_rentabilidade)
            #empresa
            try:
                empresa = info_head.find('h3', {'class':'flex-stack font-size--s0'})
                empresa = empresa.text
                empresa = empresa.replace(',','.')
            except:
                empresa = None
            list_resultado_empresa.append(empresa)
            #tipo
            try:
                tipo = info_head.find('h4', {'class':'badge'}).text
            except:
                tipo = None
            list_resultado_tipo.append(tipo)
            #tag
            try:
                tag_classificacao = info_head.find('span',{'class':'certification__tag'}).text
            except:
                tag_classificacao = info_head.find('span',{'class':'certification__tag'})
            list_resultado_tag.append(tag_classificacao)
            # --section
            info_section = card.find('section')
            table = info_section.find('table')
            tbody = table.find('tbody')
            #rentabilidade_ano
            try:
                rentabilidade_ano = tbody.find('th', text=re.compile('Rentabilidade líquida ao ano'))
                rentabilidade_ano = rentabilidade_ano.find_next('td').text
                rentabilidade_ano = rentabilidade_ano.replace(',', '.')
            except:
                rentabilidade_ano = None
            list_resultado_rentabilidade_ano.append(rentabilidade_ano)
            #prazo_resgate
            try:
                prazo_resgate = tbody.find('th', text=re.compile('Prazo de resgate'))
                prazo_resgate = prazo_resgate.find_next('td').text
            except:
                prazo_resgate = None
            list_resultado_prazo.append(prazo_resgate)
            #distribuidor
            try:
                distribuidor = tbody.find('th', text=re.compile('Distribuidor'))
                distribuidor = distribuidor.find_next('td').text
            except:
                distribuidor = None
            list_resultado_distribuidor.append(distribuidor)
            #emissor
            try:
                emissor = tbody.find('th', text=re.compile('Emissor'))
                emissor = emissor.find_next('td').text
            except:
                emissor = None
            list_resultado_emissor.append(emissor)

        dict_dados = {'retorno':list_resultado_retorno,'rentabilidade':list_resultado_rentabilidade,
                      'empresa': list_resultado_empresa, 'tag': list_resultado_tag,'tipo':list_resultado_tipo,
                      'retabilidade_ano': list_resultado_rentabilidade_ano,'prazo': list_resultado_prazo,
                      'distribuidor':list_resultado_distribuidor,'emissor':list_resultado_emissor}

        return dict_dados

if __name__ == "__main__":
    start = bate_lista_cdb_outros()

    for page in range(1, 21):
        start.inicio(page,6)