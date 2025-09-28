from django.shortcuts import render

# Create your views here.
def index_page(req):
    context = {
        'message': 'Моя Головна сторінка!'
    }
    return render(req, 'myapp/index.html', context=context)