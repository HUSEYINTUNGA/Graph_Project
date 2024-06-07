from itertools import permutations
from django.shortcuts import render
import networkx as nx
from geopy.distance import geodesic
from .models import InfoOfArea


def Anasayfa(request):
    areas = InfoOfArea.objects.all()
    path = None
    oneriler=[]
    shortest_length = float('inf')
    sehirler=[]
    if request.method == 'POST':
        G = nx.read_graphml("rehberApp/graph.graphml")
        if not G:
            return render(request, 'Anasayfa.html', {'error': 'Error reading graph data', 'locations': areas})

        city = request.POST.get('city')
        area1 = request.POST.get('area1')
        area2 = request.POST.get('area2')
        area3 = request.POST.get('area3')
        selected_areas = [city, area1, area2, area3, city]
        
        shortest_path = None
        
        for perm in permutations(selected_areas[1:-1]):
            temp_path = [selected_areas[0]] + list(perm) + [selected_areas[0]]
            temp_length = 0
            temp_path_with_cities = []
            for i in range(len(temp_path) - 1):
                try:
                    path = nx.shortest_path(G,temp_path[i], temp_path[i + 1], weight='weight')
                    length = sum(G.edges[path[i], path[i + 1]]['weight'] for i in range(len(path) - 1))
                    temp_length += length
                    
                    city = G.nodes[temp_path[i]].get('sehir', 'Bilgi yok')
                    temp_path_with_cities.append((temp_path[i], city, length))
                except nx.NetworkXNoPath:
                    break
            else:
                if temp_length < shortest_length:
                    shortest_length = temp_length
                    shortest_path = temp_path_with_cities
            path=shortest_path
            
    if path is not None:
        for sehir in path[1:4]:
            sehirler.append(sehir)
            
        for sehir in sehirler:
            onerilen_alanlar = []
            for node, data in G.nodes(data=True):
                if data.get('sehir') == sehir[1] and data.get('kategori')!='Şehir':
                    
                    info_of_area = InfoOfArea.objects.filter(name=node).first()
                    if info_of_area:
                        image_url = info_of_area.imageUrl
                    else:
                        image_url = None
                    onerilen_alanlar.append((node, data.get('sehir'), image_url))
            oneriler.extend(onerilen_alanlar)
    
    print('Oneriler ',oneriler)


    return render(request, 'Anasayfa.html', {'path': path, 'shortest_length':shortest_length,'locations': areas,'oneriler':oneriler})

        
        

def AboutWe(request):
    return render(request,'AboutWe.html')

def location(request, location_name):
    location = InfoOfArea.objects.get(name=location_name)  
    return render(request, 'Location.html', {'location': location})




