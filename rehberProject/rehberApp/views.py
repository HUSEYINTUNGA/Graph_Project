from django.shortcuts import render
import networkx as nx
def Anasayfa(request):
    path = None
    if request.method == 'POST':
        G = nx.read_graphml("rehberApp\\graph.graphml")
        start = request.POST.get('start')
        end1 = request.POST.get('end1')
        end2 = request.POST.get('end2')
        path1 = nx.shortest_path(G, source=start, target=end1, weight='weight')
        path2 = nx.shortest_path(G, source=end1, target=end2, weight='weight')
        path_nodes = path1 + path2[1:]
        
       
        path = [(node, G.nodes[node]['sehir']) for node in path_nodes]

    return render(request, 'Anasayfa.html', {'path': path})

def AboutWe(request):
    return render(request,'AboutWe.html')




