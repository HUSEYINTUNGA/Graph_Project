from django.shortcuts import render
import networkx as nx
from .models import InfoOfArea 
def Anasayfa(request):
    path = None
    areas = InfoOfArea.objects.all()  

    if request.method == 'POST':
        G = nx.read_graphml("rehberApp\\graph.graphml")
        start = request.POST.get('start')
        end1 = request.POST.get('end1')
        end2 = request.POST.get('end2')
        path1 = nx.shortest_path(G, source=start, target=end1, weight='weight')
        path2 = nx.shortest_path(G, source=end1, target=end2, weight='weight')
        path_nodes = path1 + path2[1:]
        path = [(node, G.nodes[node]['sehir']) for node in path_nodes]

    return render(request, 'Anasayfa.html', {'path': path, 'locations': areas})

def AboutWe(request):
    return render(request,'AboutWe.html')

def location(request, location_name):
    location = InfoOfArea.objects.get(name=location_name)  
    return render(request, 'Location.html', {'location': location})



