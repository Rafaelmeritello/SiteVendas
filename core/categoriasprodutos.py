categorias = {

    'informatica': ['Notebook','Armazenamento', 'Processador', 'Memoria-Ram', 'Computador', 'Monitor', 'Outros'],

    'video-game': ['Xbox-One', 'Xbox-Series X/S', 'PS4', 'PS5'],

    'telefone-celular': ['Bateria','Carregador','Celular'],

    'imovel': ['Casa','Apartamento', 'Box', 'Sala'],

    "saude-fitness": ['Suplementos','Equipamentos', 'Remedios'],

    'casa-mobilia': ['Mesas','Estante','Cadeira','Fogão','Geladeira','Secadora', 'Maquina De Lavar', 'Cama'],

    'veiculo': ['Carro','Moto','Bicicleta','Patinete','Skate', 'Outros'],

    'jogo': ['Midia-Fisica', 'Midia-Digital'],


}








def getsubcategorias(categoria):
    return categorias.get(categoria)
    pass



def getcategorias(form = False):
    choices = []
    if form:
        choices.append(("Selecione um Item", "Selecione um Item"))
    for categoria in categorias.keys():
        choices.append((categoria.lower(),categoria.capitalize().replace('-','/')))
        pass
    return choices
    pass