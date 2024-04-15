import asyncio
import aiohttp
import time


class Busca():
    def __init__(self, frase_pesquisa:str, total_paginas:int=15) -> None:
        self.total_paginas = total_paginas
        self.lista_urls = self.cria_lista_urls(frase_pesquisa)
        asyncio.run(self.resquest_async())
        print("Feito")

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
        print(lista_urls)
        return lista_urls
    

    async def resquest_async(self):
        async with aiohttp.ClientSession() as session:
            ret = await asyncio.gather(*(self.lista_produtos(url, session) for url in self.lista_urls))
        print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))

    
    async def lista_produtos(self, url:str, session):
        try:
            async with session.get(url=url) as response:
                resp = await response.read()
                print(f"Url {url} pega com sucesso !")
        except Exception as e:
            print(f"Não foi possivel pegar a url {url} por uma Exception de {e.__class__}")


    





#Busca("Tenis Fila Kr6")