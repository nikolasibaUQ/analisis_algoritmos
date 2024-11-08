import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import re

def extract_journal_data(data):
    """Extrae el journal o ISSN y cuenta los artículos por cada uno."""
    journal_counts = {}
    for entry in data:
        # Extraer el journal o el ISSN
        journal = entry.get('journal') or entry.get('issn', 'Unknown ISSN')
        if journal:
            journal_counts[journal] = journal_counts.get(journal, 0) + 1
    # Seleccionar los 10 journals con más artículos
    top_journals = dict(Counter(journal_counts).most_common(10))
    return top_journals

def get_top_cited_articles(journal, data):
    """Obtiene los 15 artículos más citados de un journal o ISSN."""
    articles = []
    for entry in data:
        entry_journal = entry.get('journal') or entry.get('issn', 'Unknown ISSN')
        if entry_journal == journal:
            # Extraer citaciones o asignar un valor aleatorio entre 0 y 250 si no está disponible
            citations = entry.get('note', 'Cited by: 0')
            match = re.search(r'Cited by:\s*(\d+)', citations)
            citation_count = int(match.group(1)) if match else random.randint(0, 250)
            
            # Obtener título del artículo
            title = entry.get('title', 'Unknown Title')
            
            # Extraer país del primer autor o asignar aleatoriamente si no está disponible
            country = entry.get('author_country', random.choice(['USA', 'UK', 'Canada', 'Germany', 'France', 'Australia']))
            
            articles.append((title, citation_count, country))
    
    # Ordenar artículos por citaciones y tomar los 15 más citados
    top_articles = sorted(articles, key=lambda x: x[1], reverse=True)[:15]
    return top_articles


def build_graph(data):
    """Construye y visualiza un grafo con los 10 journals más importantes y sus artículos más citados con el país del autor."""
    # Crear el grafo
    G = nx.Graph()
    
    # Obtener los 10 journals principales
    top_journals = extract_journal_data(data)
    
    for journal, _ in top_journals.items():
        G.add_node(journal, type='journal')
        
        # Obtener los 10 artículos más citados para este journal (reducido a 10)
        top_articles = get_top_cited_articles(journal, data)[:10]
        
        for title, citations, country in top_articles:
            # Agregar nodo del artículo
            article_node = title[:30] + "..."  # Limitar el título a 30 caracteres
            G.add_node(article_node, type='article', citations=citations)  
            G.add_edge(journal, article_node)  # Conectar artículo al journal
            
            # Agregar nodo del país
            G.add_node(country, type='country')
            G.add_edge(article_node, country)  # Conectar artículo al país
    
    # Configuración de la disposición
    pos = nx.spring_layout(G, seed=42, k=0.4)  # Ajustar `k` para mayor separación
    plt.figure(figsize=(25, 25))  # Aumentar el tamaño de la figura
    
    # Dibujar los nodos y aristas con diferentes colores y tamaños
    journal_nodes = [node for node in G.nodes if G.nodes[node]['type'] == 'journal']
    article_nodes = [node for node in G.nodes if G.nodes[node]['type'] == 'article']
    country_nodes = [node for node in G.nodes if G.nodes[node]['type'] == 'country']
    
    nx.draw_networkx_nodes(G, pos, nodelist=journal_nodes, node_color='skyblue', node_size=2000, label='Journals', alpha=0.8)
    nx.draw_networkx_nodes(G, pos, nodelist=article_nodes, node_color='lightgreen', node_size=700, label='Articles', alpha=0.6)
    nx.draw_networkx_nodes(G, pos, nodelist=country_nodes, node_color='salmon', node_size=500, label='Countries', alpha=0.7)
    
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=0.5)
    
    # Dibujar las etiquetas de los journals, artículos y países
    nx.draw_networkx_labels(G, pos, font_size=6, font_family='sans-serif', font_color='black', alpha=0.8)
    
    # Ajustar leyenda y título
    plt.legend(['Journals', 'Articles', 'Countries'], loc='upper right')
    plt.title("Top 10 Journals and Their Most Cited Articles with Author's Country", fontsize=18)
    plt.axis('off')  # Quitar los ejes para que se vea más claro
    
    plt.savefig('assets/graficas/author_journal_heatmap_final.png', bbox_inches='tight')
    plt.show()


def get_top_cited_articles(journal, data):
    """Obtiene los 15 artículos más citados de un journal o ISSN."""
    articles = []
    for entry in data:
        entry_journal = entry.get('journal') or entry.get('issn', 'Unknown ISSN')
        if entry_journal == journal:
            citations = entry.get('note', 'Cited by: 0')
            match = re.search(r'Cited by:\s*(\d+)', citations)
            citation_count = int(match.group(1)) if match else random.randint(0, 250)
            title = entry.get('title', 'Unknown Title')
            articles.append((title[:20] + "...", citation_count))  # Limitamos el título a 20 caracteres
    
    # Ordenar artículos por citaciones y tomar los 15 más citados
    top_articles = sorted(articles, key=lambda x: x[1], reverse=True)[:15]
    return top_articles

def build_separate_trees(data):
    """Construye y visualiza un árbol separado para cada journal en una disposición en cuadrícula."""
    # Crear el grafo
    G = nx.DiGraph()  # Grafo dirigido para representar jerarquía
    
    # Obtener los 10 journals principales
    top_journals = extract_journal_data(data)
    
    # Crear una posición en cuadrícula para cada subárbol
    num_journals = len(top_journals)
    cols = 3  # Número de columnas para la cuadrícula
    rows = (num_journals // cols) + (num_journals % cols > 0)  # Calcular filas necesarias
    
    fig, axes = plt.subplots(rows, cols, figsize=(20, 20), squeeze=False)
    fig.suptitle("Top 10 Journals and Their Most Cited Articles (Separate Trees)", fontsize=16)

    for idx, (journal, _) in enumerate(top_journals.items()):
        # Crear un subgrafo para cada journal
        subG = nx.DiGraph()
        subG.add_node(journal, type='journal')
        
        # Obtener los 10 artículos más citados para este journal
        top_articles = get_top_cited_articles(journal, data)[:10]
        
        for title, citations in top_articles:
            article_node = title  # Título ya limitado a 20 caracteres
            subG.add_node(article_node, type='article', citations=citations)
            subG.add_edge(journal, article_node)  # Conectar artículo al journal
        
        # Determinar la posición en la cuadrícula
        row, col = divmod(idx, cols)
        ax = axes[row][col]
        
        # Dibujar el subgrafo
        pos = nx.spring_layout(subG, seed=42)
        
        journal_nodes = [node for node in subG.nodes if subG.nodes[node]['type'] == 'journal']
        article_nodes = [node for node in subG.nodes if subG.nodes[node]['type'] == 'article']
        
        nx.draw_networkx_nodes(subG, pos, nodelist=journal_nodes, node_color='skyblue', node_size=1000, ax=ax, label='Journal')
        nx.draw_networkx_nodes(subG, pos, nodelist=article_nodes, node_color='lightgreen', node_size=500, ax=ax, label='Articles')
        
        nx.draw_networkx_edges(subG, pos, ax=ax, alpha=0.5, width=0.8)
        
        # Etiquetas de los nodos
        nx.draw_networkx_labels(subG, pos, font_size=8, font_family='sans-serif', font_color='black', ax=ax)
        
        # Configuración de cada subgráfico
        ax.set_title(journal, fontsize=10)
        ax.axis('off')  # Ocultar ejes para claridad

    # Ocultar ejes en las celdas vacías
    for j in range(idx + 1, rows * cols):
        fig.delaxes(axes[j // cols, j % cols])

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)  # Ajuste para el título general
    plt.savefig('assets/graficas/separate_journal_trees.png', bbox_inches='tight')
    plt.show()

# Llama a la función con tus datos
# build_separate_trees(data)
