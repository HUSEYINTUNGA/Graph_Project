from django.shortcuts import render
import networkx as nx
def Anasayfa(request):
    return render(request,'anasayfa.html')





def shortest_path(request):
    G = nx.read_gpickle("graph.graphml")
    if request.method == 'POST':
        start = request.POST.get('start')
        end1 = request.POST.get('end1')
        end2 = request.POST.get('end2')
        path1 = nx.shortest_path(G, source=start, target=end1, weight='weight')
        path2 = nx.shortest_path(G, source=end1, target=end2, weight='weight')
        path = path1 + path2[1:]  
        return render(request, 'shortest_path.html', {'path': path})
    else:
        return render(request, 'shortest_path.html')
