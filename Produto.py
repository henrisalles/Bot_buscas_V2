link_produto = []

class Produto:
    def __init__(self, soup) -> None:
        self.soup = soup
        self.nome, self.preco, self.vendedor, self.tipo_anuncio, self.url_imagem, self.cor, self.quantidade  = self.get_attributes()

        print(self.preco)
        print(self.vendedor)
    
    def get_attributes(self):
        nome = self.soup.find("div", class_="ui-pdp-header__title-container").find("h1","ui-pdp-title").text
        frame_preco = self.soup.find("div", class_="ui-pdp-price__main-container")
        preco = float(frame_preco.find("span", class_="andes-money-amount__fraction").text + "." + frame_preco.find("span", class_="andes-money-amount__cents andes-money-amount__cents--superscript-16").text)
        vendedor = self.soup.find("span", class_="ui-pdp-color--BLUE ui-pdp-family--REGULAR").text
        
        try:
            tipo_anuncio = None
        except:
            tipo_anuncio = None       
        url_imagem = None
        cor = None
        quantidade = None

        return nome, preco, vendedor, tipo_anuncio, url_imagem, cor, quantidade