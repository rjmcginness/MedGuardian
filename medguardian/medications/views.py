from django.shortcuts import render


def index(request):
    name = request.GET.get('name') or ''

    return render(request, 'base.html', {'name': name})

def medication_search(request):
    search_words = request.GET.getlist('q')

    return render(request, 'medication-search.html', {'search_words': search_words})