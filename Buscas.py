import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
from Produto import ProdutoML


class BuscaML():
    def __init__(self, frase_pesquisa:str, palavras_chave:list, palavras_chave_exclusora:list, total_paginas:int=1) -> None:
        """ 
        Realiza todas as buscas necessárias para a aquisição das informações/propriedades dos produtos
        """
        self.__lista_pagina_lista_produto = []
        self.__lista_pagina_produto = []
        self.lista_produtos = []
        self.lista_urls_pagina_produto = []

        self.total_paginas = total_paginas
        # Cria uma lista de url para cada pagina_lista de produtos
        self.lista_urls_pagina_lista_produto = self.__cria_lista_urls(frase_pesquisa)
        # Realiza as requests assincronas das paginas lista
        asyncio.run(self.__resquest_async(self.lista_urls_pagina_lista_produto, self.__lista_pagina_lista_produto))
        # Realiza a procura do url do produto no html da request
        self.__procura_url_produto_em_pagina_lista(palavras_chave, palavras_chave_exclusora)
        # Realiza as requests assincronas das paginas produto
        asyncio.run(self.__resquest_async(self.lista_urls_pagina_produto, self.__lista_pagina_produto))
        # Realiza a classificação dos produtos
        self.__procura_atributos_na_url_produto()


    def __cria_lista_urls(self, frase_pesquisa:str):
        """ 
        Cria uma lista com as urls das paginas de listagem de produto
        Return: lista_urls <type:list>
        """
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
    
    async def __resquest_async(self, lista_urls, lista_p_append):
        async with aiohttp.ClientSession() as session:
            ret = await asyncio.gather(*(self.__lista_requests(url, session, lista_p_append) for url in lista_urls))
        print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))

    async def __lista_requests(self, url:str, session, lista:list):
        try:
            async with session.get(url=url) as response:
                resp = await response.text()
                lista.append([resp, url])
                #print(f"Url {url} pega com sucesso !")
            return response
        except Exception as e:
            #print(f"Não foi possivel pegar a url {url} por uma Exception de {e.__class__}")
            pass

    def __procura_url_produto_em_pagina_lista(self, palavras_chave, palavras_chave_exclusora):
        """ 
        Itera pelas peginas de listagem de produtos, realiza a conferencia de urls não repetidas e já realiza o append na self.lista_urls_pagina_produto
        Além de realizar a verificação das palavras chave no nome do anuncio/produto
        Return: None
        """
        urls_produtos = []
        for pagina in self.__lista_pagina_lista_produto:
            soup = BeautifulSoup(pagina[0], "html.parser")
            search_frames = soup.find_all('li', class_="ui-search-layout__item")
            # Limitando o search_frame para o padrao de busca por pagina
            search_frames = search_frames[:40]
            for prod in search_frames:
                # Confere palavras chave e exclusoras
                produto_valido = True
                nome_prod = prod.find("h2", class_="ui-search-item__title").text
                nome_prod_split = nome_prod.lower().split()
                for palavra in palavras_chave:
                    if palavra.lower() not in nome_prod_split:
                        produto_valido = False
                        break
                for palavra in palavras_chave_exclusora:
                    if palavra.lower() in nome_prod_split:
                        produto_valido = False
                        break
                if produto_valido:
                    urls_produtos.append(prod.find('a', class_='ui-search-link')['href'])

        # Realizando conferencia antes das requests se não há urls repetidas
        for i in range(len(urls_produtos)):
            if urls_produtos[i] not in self.lista_urls_pagina_produto:
                self.lista_urls_pagina_produto.append(urls_produtos[i])
        

    def __procura_atributos_na_url_produto(self):
        """
        Itera por cada pagina html dos produtos e criar os objetos class Produto retornando uma lista com os mesmos
        Return: None 
        """
        for pagina_produto in self.__lista_pagina_produto:
            soup = BeautifulSoup(pagina_produto[0], "html.parser")
            self.lista_produtos.append(ProdutoML(soup, pagina_produto[1], "Mercado Livre"))
