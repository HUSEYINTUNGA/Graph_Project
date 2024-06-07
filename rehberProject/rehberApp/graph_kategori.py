import mysql.connector
import networkx as nx
from geopy.distance import geodesic

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="ht.123456.",
    database="turistikbolgeler"
)

mycursorOne = mydb.cursor()
mycursorOne.execute("SELECT * FROM bolgeler")
rows = mycursorOne.fetchall()



G_kategori=nx.Graph()

kategori_renkleri = {
    'Tarihi Yapı': 'yellow',
    'Su Bölgesi': 'blue',
    'Beşeri Unsur': 'orange',
    'Doğal Oluşum': 'green',
    
}


categories=['Doğal Oluşum','Beşeri Unsur','Tarihi Yapı','Su Bölgesi']
for category in categories:
    G_kategori.add_node(category,ad=category,kategori='kategori', color=kategori_renkleri[category])
    
for row in rows:
    G_kategori.add_node(row[0],ad=row[0],kategori=row[4],color=kategori_renkleri[row[4]])    
    
for node1 in G_kategori.nodes():
    if G_kategori.nodes[node1]['kategori']=='kategori':
        for node2 in G_kategori.nodes():
            if G_kategori.nodes[node2]['kategori']==G_kategori.nodes[node1]['ad'] and G_kategori.nodes[node2]['ad']!=G_kategori.nodes[node1]['ad']:
                G_kategori.add_edge(node1,node2, color=kategori_renkleri[G_kategori.nodes[node2]['kategori']], relationship='Kategorisinde')      
            elif G_kategori.nodes[node2]['kategori']=='kategori' and node1 != node2:
                G_kategori.add_edge(node1,node2, color='black')

nx.write_graphml(G_kategori, "graph_kategori.graphml")