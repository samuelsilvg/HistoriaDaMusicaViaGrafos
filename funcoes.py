import csv
import networkx as nx
from classes import Artista
from collections import Counter, deque

def criar_artistas():

    lista_artistas = []

    with open('BSMA.csv', 'r') as file:
        reader = csv.DictReader(file)
        dados = list(reader)

    for linha in dados:
        artista = linha['Artist name']
        pais = linha['Country'].split("/")
        atividade = linha['period_active'].split("–")
        linha['Year'] = int(linha['Year'])
        debut = linha['Year']
        lista_generos = linha['Genre'].split("/")
        vendas = linha['Sales']

        banda = Artista(artista, pais, lista_generos, atividade, debut, vendas)
        lista_artistas.append(banda)

    return sorted(lista_artistas, key=lambda artista: artista.debut)

def separar_artistas_decada(artistas, decada):
    lista_artistas_decada = []

    for artista in artistas:
        if (artista.debut // 10) == decada // 10:
            lista_artistas_decada.append(artista)

    return lista_artistas_decada

def comparar_artistas(artista1, artista2):
    peso = 0
    padroes = {
        "mesma_decada": None,
        "mesmo_pais": [],
        "mesmo_genero": [],
    }

    # Mesma década de estreia
    if artista1.debut // 10 == artista2.debut // 10:
        peso += 1
        padroes["mesma_decada"] = artista1.debut // 10 * 10

    # Mesmo país de origem
    paises_em_comum = list(set(artista1.pais) & set(artista2.pais))
    if any(pais in artista2.pais for pais in artista1.pais):
        peso += 1
        padroes["mesmo_pais"] = paises_em_comum

    # Mesmo gênero musical
    generos_em_comum = list(set(artista1.generos) & set(artista2.generos))
    if any(genero in artista2.generos for genero in artista1.generos):
        peso += 1
        padroes["mesmo_genero"] = generos_em_comum

    return peso, padroes

def exportar_para_gephi(grafo, nome_arquivo_nodes, nome_arquivo_edges):

    # Exportar os nós
    with open(nome_arquivo_nodes, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Id', 'Label'])  # Cabeçalho
        
        for node in grafo.nodes():
            writer.writerow([node, node])  # ID e Label são o nome do artista

    # Exportar as arestas
    with open(nome_arquivo_edges, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Source', 'Target', 'Weight', 'Decada', 'Pais', 'Genero'])  # Cabeçalho atualizado
        
        for source, target, data in grafo.edges(data=True):
            weight = data.get('weight', 1)  # Peso da conexão
            decada = data.get('mesma_decada', 'Desconhecido')  # Década compartilhada
            pais = ', '.join(data.get('mesmo_pais', [])) or 'Nenhum'  # Países em comum
            genero = ', '.join(data.get('mesmo_genero', [])) or 'Nenhum'  # Gêneros em comum
            
            writer.writerow([source, target, weight, decada, pais, genero])

    print(f"Arquivos '{nome_arquivo_nodes}' e '{nome_arquivo_edges}' exportados com sucesso.")

def bfs(G):
    contagem_data_por_decada = {}
    arestas_visitadas = set()  # Conjunto para evitar contagens duplicadas

    # Percorrer o grafo usando BFS a partir de cada nó
    for start_node in G.nodes():
        visitados = set()
        fila = deque([start_node])

        while fila:
            node = fila.popleft()
            if node in visitados:
                continue
            visitados.add(node)

            for vizinho in G.neighbors(node):
                if vizinho in visitados:
                    continue

                # Criar uma tupla ordenada para evitar contagem duplicada
                aresta = tuple(sorted([node, vizinho]))
                if aresta in arestas_visitadas:
                    continue  # Se já contamos essa aresta, ignoramos

                # Marcar como processada
                arestas_visitadas.add(aresta)

                # Obter dados da aresta
                data = G.get_edge_data(node, vizinho)
                decada = data.get('mesma_decada')
                peso = data.get('weight', 0)

                if decada is not None and peso >= 3:
                    data_tupla = {k: tuple(v) if isinstance(v, list) else v for k, v in data.items()}

                    if decada not in contagem_data_por_decada:
                        contagem_data_por_decada[decada] = Counter()

                    contagem_data_por_decada[decada][tuple(data_tupla.items())] += 1

                fila.append(vizinho)

    # Encontrar o top 5 das conexões mais comuns para cada década
    resultados = {}
    for decada, contagem_data in contagem_data_por_decada.items():
        top_5 = contagem_data.most_common(5)  # Obtém os 5 mais comuns
        resultados[decada] = top_5

    return resultados

def comparacao_decada(artista1, artista2):
    peso = 0

    if artista1.debut // 10 == artista2.debut // 10:
        peso += 1

    return peso

def exportar_gephi_h(grafo, nome_arquivo_nodes, nome_arquivo_edges):
    
    # Exportando os nós
    with open(nome_arquivo_nodes, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Id', 'Label'])  # Cabeçalho
            
        for node in grafo.nodes():
            writer.writerow([node, node])  # ID e Label são o nome do artista

    # Exportando as arestas
    with open(nome_arquivo_edges, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Source', 'Target', 'Weight'])  # Cabeçalho atualizado
        
        for source, target, data in grafo.edges(data=True):
            weight = data.get('weight', 1)  # Peso da conexão
            writer.writerow([source, target, weight])

    print(f"Arquivos '{nome_arquivo_nodes}' e '{nome_arquivo_edges}' exportados com sucesso.")

def modelar_grafo(G, artistas):
    for i in range(len(artistas)):
        for j in range(i+1, len(artistas)):
            peso, padroes = comparar_artistas(artistas[i], artistas[j])
            if peso > 0:
                G.add_edge(
                    artistas[i].artista, 
                    artistas[j].artista, 
                    weight=peso,
                    mesma_decada = padroes["mesma_decada"],
                    mesmo_pais=padroes["mesmo_pais"],
                    mesmo_genero=padroes["mesmo_genero"]
                )

    #labels = nx.get_edge_attributes(G,'weight')
    #edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
    #nx.draw(G, node_color='b', edge_color=weights, width=weights*100, with_labels=True)

def modelar_grafo_h(H, artistas):
    for i in range(len(artistas)):
        for j in range(i+1, len(artistas)):
            peso = comparacao_decada(artistas[i], artistas[j])
            H.add_edge(artistas[i].artista, artistas[j].artista, weight=peso)

def salvar_resultados_txt(resultados, file='resultados.txt'):
    with open(file, "w") as file:
        for decada, top_5 in resultados.items():
            file.write(f"Década: {decada}\n")
            for i, (data_mais_comum, frequencia) in enumerate(top_5, 1):
                file.write(f"  {i}. Conteúdo de aresta com weight 3: {data_mais_comum} ({frequencia} aparições)\n")
            file.write("\n")  # Adiciona uma linha em branco entre as décadas

    print(f"Resultados salvos com sucesso!")