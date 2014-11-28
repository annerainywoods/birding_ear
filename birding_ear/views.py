from django.http import HttpResponse
from django.shortcuts import render_to_response
# Import the Category model
from birding_ear.models import Bird, State, Bird_type
from json import dumps, loads


def index(request):
    bird_list = Bird.objects.order_by('name')
    context_dict = {'birds': bird_list}

    # Render the response and send it back!
    return render_to_response('index.html', context_dict)

def ajax(request):
    birds_ajax = list(Bird.objects.all())
    birds_ajax_list = []
    for b in birds_ajax:
        birds_ajax_list.append({
            "name": b.name
        })
    return HttpResponse(dumps(birds_ajax_list), content_type="application/json")






#def hello(request):
#    return HttpResponse("Hello world")