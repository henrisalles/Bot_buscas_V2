import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
from Produto import Produto


class Busca():
    def __init__(self, frase_pesquisa:str, total_paginas:int=1) -> None:
        self.lista_pagina_lista_produto = []
        self.lista_pagina_produto = []

        self.total_paginas = total_paginas
        # Cria uma lista de url para cada pagina_lista de produtos
        self.lista_urls_pagina_lista_produto = self.cria_lista_urls(frase_pesquisa)
        # Realiza as requests assincronas
        asyncio.run(self.resquest_async(self.lista_urls_pagina_lista_produto, self.lista_pagina_lista_produto))
        # Realiza a procura do url do produto no html da request
        self.lista_urls_pagina_produto = self.procura_url_produto_em_pagina_lista()
        # Realiza as requests assincronas
        asyncio.run(self.resquest_async(self.lista_urls_pagina_produto, self.lista_pagina_produto))
        
        self.procura_atributos_na_url_produto()




    def cria_lista_urls(self, frase_pesquisa:str):
        lista_frase = frase_pesquisa.split()
        frase_p_url = ""
        for i in range(len(lista_frase)):
            frase_p_url = f"{frase_p_url}-{lista_frase[i]}"
        frase_p_url = frase_p_url[1:]
        lista_urls = []
        for i in range(self.total_paginas):
            pagina_desde_x = i*40 
            lista_urls.append(f"https://lista.mercadolivre.com.br/{frase_p_url}_Desde_{pagina_desde_x}_NoIndex_True")
        return lista_urls
    
    async def resquest_async(self, lista_urls, lista_p_append):
        async with aiohttp.ClientSession() as session:
            ret = await asyncio.gather(*(self.lista_produtos(url, session, lista_p_append) for url in lista_urls))
        print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))

    async def lista_produtos(self, url:str, session, lista):
        try:
            async with session.get(url=url) as response:
                resp = await response.text()
                lista.append(resp)
                print(f"Url {url} pega com sucesso !")
                return response
        except Exception as e:
            print(f"Não foi possivel pegar a url {url} por uma Exception de {e.__class__}")

    def procura_url_produto_em_pagina_lista(self):
        for pagina in self.lista_pagina_lista_produto:
            soup = BeautifulSoup(pagina, "html.parser")
            url_produtos = []
            search_frames = soup.find_all('li', class_="ui-search-layout__item")
            # Limitando o search_frame para o padrao de busca por pagina
            search_frames = search_frames[:40]
            for prod in search_frames:
                url_produtos.append(prod.find('a', class_='ui-search-link')['href'])
        return url_produtos

    def procura_atributos_na_url_produto(self):
        for pagina_produto in self.lista_pagina_produto:
            soup = BeautifulSoup(pagina_produto, "html.parser")
            produto = Produto()
            



Busca("Tenis Fila Kr6")