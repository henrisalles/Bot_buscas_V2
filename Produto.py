import re

link_produto = []

class ProdutoML:
    def __init__(self, soup, url, marketplace) -> None:
        """
        Cria os objetos produtos com as 
        """
        self.__soup = soup
        self.marketplace = marketplace
        self.url = url
        self.nome, self.preco, self.vendedor, self.tipo_anuncio, self.url_imagem, self.cor, self.quantidade  = self.__get_attributes()
    
    def __get_attributes(self):
        """
        Lê a response html por meio do Beautifullsoup e pega cada uma das propriedades dos produtos
        Return: nome <type:str>,
                preco <type:float>,
                vendedor <type:str>,
                tipo_anuncio <type:str>,
                url_imagem <type:str>,
                cor <type:str>,
                quantidade <type:int>
        """
        nome = self.__soup.find("div", class_="ui-pdp-header__title-container").find("h1","ui-pdp-title").text
        frame_preco = self.__soup.find("div", class_="ui-pdp-price__main-container")
        preco = frame_preco.find("span", class_="andes-money-amount__fraction").text 
        try:
            preco_cents = "." + frame_preco.find("span", class_="andes-money-amount__cents andes-money-amount__cents--superscript-16").text
            preco = f"{preco}{preco_cents}"
        except:
            pass

        vendedor = self.__soup.find("span", class_="ui-pdp-color--BLUE ui-pdp-family--REGULAR").text
        
        try:
            tipo_anuncio = None
        except:
            tipo_anuncio = None       
        
        url_imagem = self.__soup.find("img", class_="ui-pdp-image ui-pdp-gallery__figure__image")['src']
        print(url_imagem)

        try:
            quantidade = self.soup.find('span', class_='ui-pdp-buybox__quantity__available').text
            quantidade = re.findall(r'\d+', quantidade)
            quantidade = quantidade[0]

        except:
            quantidade = 1

        try:
            cor = self.soup.find('span', class_='ui-pdp-variations__selected-label ui-pdp-color--BLACK').text.lower()
            cor = cor.split('/')[0]
            cor = cor.split('-')[0]
            cor = cor.split(' ')[0]
            cor = cor.split('+')[0]
            cor = cor.split(',')[0]
            if cor == 'pto' or cor == 'pta' or cor == 'preta':
                cor = 'preto'
            elif cor == 'bco' or cor == 'bca' or cor == 'branca':
                cor = 'branco'
            elif cor == 'vde' or cor == 'lim' or cor == 'lima' or cor == 'limão':
                cor = 'verde'
        except:
            cor = None

        return nome, float(preco), vendedor, tipo_anuncio, url_imagem, cor, quantidade