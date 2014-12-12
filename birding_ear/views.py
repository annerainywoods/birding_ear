from django.http import HttpResponse
from django.shortcuts import render_to_response, render
# Import the Category model
from .models import Bird, State, BirdType, UserBird, Mix, Drill
from json import dumps, loads
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# def index(request):
#    return HttpResponse("Rango says hello world!")

def index(request):
    # get list of birds from userbird that matches both state/s and type/s
    bird_list = UserBird.objects.order_by('bird__name')
    context_dict = {'birds': bird_list}

    # Render the response and send it back!
    return render_to_response('index.html', context_dict)





@csrf_exempt
def ajax(request):
    if request.method == "POST":
        bird = Bird()
        bird.user = User.objects.all()[0]
        bird.name = request.POST["name"]
        bird.save()

    birds_ajax = list(Bird.objects.all())
    birds_ajax_list = []
    for b in birds_ajax:
        birds_ajax_list.append({
            "name": b.name
        })
    return HttpResponse(dumps(birds_ajax_list), content_type="application/json")


def dom(request):
    if request.method == "POST":
        print request.POST

    return render(request, 'dom.html')



#def hello(request):
#    return HttpResponse("Hello world")