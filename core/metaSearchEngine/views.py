from django.template import RequestContext
from django.shortcuts import render
from collections import Counter
from metaSearchEngine.search import search_result

def index(request):
    if request.method == 'POST':
        query = request.POST['Search']

        title_result, src_result = search_result(query)

        return render(request, 'home/srch_res.html', {'search': zip(title_result, src_result)})

    else:
        return render(request, 'home/home.html')


