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
    mix_list = Mix.objects.order_by('nickname')
    context_dict = {'mixes': mix_list}

    # Render the response and send it back!
    return render_to_response('index.html', context_dict)


def mix_detail(request, mix_nickname_slug):
    context_dict = {}
    mix = Mix.objects.get(slug=mix_nickname_slug)
    context_dict['mix_slug'] = mix_nickname_slug
    context_dict['mix_nickname'] = mix.nickname
    context_dict['mix_description'] = mix.description
    context_dict['mix_color'] = mix.color
    context_dict['mix_states'] = mix.states.all()
    context_dict['mix_bird_types'] = mix.bird_types.all()


    if mix.bird_types.all() and mix.states.all():
        bird_list = UserBird.objects.all().filter(bird__bird_type__in=mix.bird_types.all())\
            .filter(bird__states__in=mix.states.all()).distinct()
    elif mix.bird_types.all():
        bird_list = UserBird.objects.all().filter(bird__bird_type__in=mix.bird_types.all())
    elif mix.states.all():
        bird_list = UserBird.objects.all().filter(bird__states__in=mix.states.all()).distinct()
    else:
        bird_list = UserBird.objects.all()

    context_dict['birds'] = bird_list
    return render_to_response('mix_detail.html', context_dict)

def mix_settings(request, mix_nickname_slug):
    context_dict = {}
    mix = Mix.objects.get(slug=mix_nickname_slug)
    context_dict['mix_nickname'] = mix.nickname
    context_dict['mix_description'] = mix.description
    context_dict['mix_color'] = mix.color
    context_dict['mix_states'] = mix.states.all()

    return render_to_response('mix_edit.html', context_dict)


def bird_detail(request, bird_name_slug):
    context_dict = {}
    mix_list = {}
    bird = UserBird.objects.get(slug=bird_name_slug)
    context_dict['bird_name'] = bird.bird.name
    context_dict['bird_call'] = bird.bird.bird_call
    context_dict['bird_type'] = bird.bird.bird_type
    if bird.favorite:
        context_dict['favorite'] = "checked=checked"
    if bird.favorite:
        context_dict['excluded'] = "checked=checked"
    context_dict['bird_pile'] = bird.bird_pile
    #mix-list needs API
    return render_to_response('bird_detail.html', context_dict)


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