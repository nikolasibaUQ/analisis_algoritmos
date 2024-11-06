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

