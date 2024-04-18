from Buscas import BuscaML

nome_produto = "Tenis fila kr6"
palavra_chave = ["fila", "kr6"]
palavra_chave_exclusora = ["kenya"]

busca_ml = BuscaML(nome_produto, palavra_chave, palavra_chave_exclusora)


for prod in busca_ml.lista_produtos:
    print(prod.nome)