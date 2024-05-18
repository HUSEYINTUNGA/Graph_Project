import networkx as nx
import mysql.connector
from geopy.distance import geodesic


mydb = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="ht.123456.",
    database="turistikbolgeler"
)

mycursor = mydb.cursor()


mycursor.execute("SELECT * FROM turistikbolgeler.bolgeler")
myresult = mycursor.fetchall()


G = nx.Graph()

for row in myresult:
    G.add_node(row[0], sehir=row[1], lat=float(row[2]), lon=float(row[3]), kategori=row[4])

for node1 in G.nodes():
    for node2 in G.nodes():
        if node1 != node2:
            lat1, lon1 = float(G.nodes[node1]["lat"]), float(G.nodes[node1]["lon"])
            lat2, lon2 = float(G.nodes[node2]["lat"]), float(G.nodes[node2]["lon"])
            distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
            if distance < 200:
                G.add_edge(node1, node2, weight=distance)


nx.write_graphml(G, "graph.graphml")
