class Artista:

    def __init__(self, artista, pais, generos, atividade, debut, vendas):
        self.artista = artista
        self.pais = pais
        self.atividade = atividade
        self.debut = debut
        self.generos = generos
        self.vendas = vendas
        

    def __str__(self):
        return f'{self.artista} | {self.generos} | {self.pais} | {self.atividade}'