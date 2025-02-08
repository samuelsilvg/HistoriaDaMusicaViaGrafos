import networkx as nx

from funcoes import criar_artistas
from funcoes import separar_artistas_decada
from funcoes import modelar_grafo_h
from funcoes import modelar_grafo
from funcoes import exportar_gephi_h
from funcoes import exportar_para_gephi
from funcoes import bfs
from funcoes import salvar_resultados_txt

# Criação dos grafos que serão usados
H = nx.Graph()
G = nx.Graph()
G_1960 = nx.Graph()
G_1970 = nx.Graph()
G_1980 = nx.Graph()
G_1990 = nx.Graph()
G_2000 = nx.Graph()
G_2010 = nx.Graph()

# Criação da lista de artistas, extraídos da database BSMA
artistas = criar_artistas()

# Separação da lista de artistas em novas listas por década
artistas_1960 = separar_artistas_decada(artistas, 1960)
artistas_1970 = separar_artistas_decada(artistas, 1970)
artistas_1980 = separar_artistas_decada(artistas, 1980)
artistas_1990 = separar_artistas_decada(artistas, 1990)
artistas_2000 = separar_artistas_decada(artistas, 2000)
artistas_2010 = separar_artistas_decada(artistas, 2010)

# Modelagem de cada grafo com base em seus parâmetros
modelar_grafo_h(H, artistas)
modelar_grafo(G, artistas)
modelar_grafo(G_1960, artistas_1960)
modelar_grafo(G_1970, artistas_1970)
modelar_grafo(G_1980, artistas_1980)
modelar_grafo(G_1990, artistas_1990)
modelar_grafo(G_2000, artistas_2000)
modelar_grafo(G_2010, artistas_2010)

# Exportação dos grafos em CSVs para inserção no Gephi
exportar_gephi_h(H, 'gephi_csvs/nodes_h.csv', 'gephi_csvs/egdes_h.csv')
exportar_para_gephi(G,'gephi_csvs/nodes.csv', 'gephi_csvs/edges.csv')
exportar_para_gephi(G_1960,'gephi_csvs/nodes_1960.csv', 'gephi_csvs/edges_1960.csv')
exportar_para_gephi(G_1970, 'gephi_csvs/nodes_1970.csv', 'gephi_csvs/edges_1970.csv')
exportar_para_gephi(G_1980, 'gephi_csvs/nodes_1980.csv', 'gephi_csvs/edges_1980.csv')
exportar_para_gephi(G_1990, 'gephi_csvs/nodes_1990.csv', 'gephi_csvs/edges_1990.csv')
exportar_para_gephi(G_2000, 'gephi_csvs/nodes_2000.csv', 'gephi_csvs/edges_2000.csv')
exportar_para_gephi(G_2010, 'gephi_csvs/nodes_2010.csv', 'gephi_csvs/edges_2010.csv')

# Implementação do algoritmo BFS no grafo principal
resultados_por_decada_weight_3 = bfs(G)
salvar_resultados_txt(resultados_por_decada_weight_3)