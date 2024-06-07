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
mycursorTwo = mydb.cursor()
mycursorTwo.execute("SELECT * FROM sehirler")
cities=mycursorTwo.fetchall()

G = nx.Graph()
G_kategori=nx.Graph()

kategori_renkleri = {
    'Tarihi Yapı': 'yellow',
    'Su Bölgesi': 'blue',
    'Beşeri Unsur': 'orange',
    'Doğal Oluşum': 'green',
    'Şehir':'red'
}

for row in rows:
    G.add_node(row[0],ad=row[0], sehir=row[1], lat=float(row[2]), lon=float(row[3]), kategori=row[4], color=kategori_renkleri[row[4]])
for city in cities:
    G.add_node(city[0],ad=city[0],sehir=city[0],lat=float(city[1]),lon=float(city[2]),kategori='Şehir',color='red')

for node1 in G.nodes():
    for node2 in G.nodes():
        #Şehir-Şehir
        if (G.nodes[node1]['kategori'] =='Şehir' and G.nodes[node2]['kategori']=='Şehir') and ((G.nodes[node1]['ad'] != G.nodes[node2]['ad'])):
            lat1, lon1 = float(G.nodes[node1]["lat"]), float(G.nodes[node1]["lon"])
            lat2, lon2 = float(G.nodes[node2]["lat"]), float(G.nodes[node2]["lon"])
            distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
            if distance<200:
                G.add_edge(node1,node2, color=kategori_renkleri['Şehir'],weight=distance)
            
        #Şehir-Alan 
        elif (G.nodes[node1]['kategori'] =='Şehir' and G.nodes[node2]['kategori']!='Şehir'):
            if G.nodes[node2]['sehir']==G.nodes[node1]['ad']:
                lat1, lon1 = float(G.nodes[node1]["lat"]), float(G.nodes[node1]["lon"])
                lat2, lon2 = float(G.nodes[node2]["lat"]), float(G.nodes[node2]["lon"])
                distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
                G.add_edge(node2,node1, color='black', relationship='Aittir',weight=distance)
        
        #Alan-Alan
        elif G.nodes[node1]['kategori']!='Şehir' and  G.nodes[node2]['kategori']!='Şehir':
            if ((G.nodes[node1]['ad'] != G.nodes[node2]['ad'])):
                lat1, lon1 = float(G.nodes[node1]["lat"]), float(G.nodes[node1]["lon"])
                lat2, lon2 = float(G.nodes[node2]["lat"]), float(G.nodes[node2]["lon"])
                distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
                    
                if G.nodes[node1]['kategori'] == G.nodes[node2]['kategori'] and distance < 300:
                    G.add_edge(node1,node2, color=kategori_renkleri[G.nodes[node1]['kategori']],weight=distance, relationship='aynı kategori')

nx.write_graphml(G, "graph.graphml")
