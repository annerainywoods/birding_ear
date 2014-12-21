from django.http import HttpResponse
from django.shortcuts import render_to_response, render
# Import the Category model
from .models import Bird, State, BirdType, UserBird, Mix, Drill
from json import dumps, loads
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def register(request):
    if request.method == "POST":
        user = User.objects.create_user(request.POST["username"], None, request.POST["password"])
        for b in Bird.objects.all():
            ub = UserBird()
            ub.bird = b
            ub.user = user
            ub.save()
    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        user = auth.authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                print("User is valid, active and authenticated")
                return redirect('index')
            else:
                print("The password is valid, but the account has been disabled!")

        else:
            print("the password is valid, but the account has been disabled!")

    else:
        print("the username and password were incorrect.")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return render(request, 'login.html')


@login_required
def index(request):
    print request.user
    mix_list = Mix.objects.filter(user=request.user)
    context_dict = {'mixes': mix_list}
    context = RequestContext(request)

    # Render the response and send it back!
    return render_to_response('index.html', context_dict, context)


@login_required
def mix_detail(request, mix_nickname_slug):
    context_dict = {}
    mix = Mix.objects.get(slug=mix_nickname_slug)
    context_dict['mix_slug'] = mix_nickname_slug
    context_dict['mix_nickname'] = mix.nickname
    context_dict['mix_description'] = mix.description
    context_dict['mix_color'] = mix.color
    context_dict['mix_states'] = mix.states.all()
    context_dict['mix_bird_types'] = mix.bird_types.all()
    context_dict['bird_list'] = mix.bird_list
    context_dict['num_learned'] = mix.num_learned
    context = RequestContext(request)
    return render_to_response('mix_detail.html', context_dict, context)


@login_required
def mix_settings_edit(request, mix_nickname_slug):
    context_dict = {}
    mix = Mix.objects.get(slug=mix_nickname_slug)
    if request.method == "POST":
        mix.nickname = request.POST["nickname"]
        mix.description = request.POST["description"]
        mix.color = request.POST["color"]
        mix.user = request.user
        mix.save()
        mix_nickname_slug = mix.slug
        return redirect('/mix_detail/' + mix_nickname_slug)
    else:
        context_dict['mix_nickname'] = mix.nickname
        context_dict['mix_description'] = mix.description
        context_dict['mix_color'] = mix.color
        context_dict['mix_states'] = mix.states
        context_dict['state_options'] = State.objects.all()
        context_dict['type_options'] = BirdType.objects.all()
        context_dict['slug'] = mix.slug

        context = RequestContext(request)
        return render_to_response('mix_edit.html', context_dict, context)


@login_required
def mix_settings_new(request):
    mix = Mix()
    if request.method == "POST":
        mix.nickname = request.POST["nickname"]
        mix.description = request.POST["description"]
        mix.color = request.POST["color"]
        mix.user = request.user
        mix.save()
        mix_nickname_slug = mix.slug
        return redirect('/mix_detail/' + mix_nickname_slug)
    else:
        context_dict = {}
        context_dict['mix_color'] = "TGY"
        context_dict['state_options'] = State.objects.all()
        context_dict['type_options'] = BirdType.objects.all()
        context = RequestContext(request)
        return render_to_response('mix_edit.html', context_dict, context)


    # context_dict = {}
    # context_dict['mix_nickname'] = mix.nickname
    # context_dict['mix_description'] = mix.description
    # context_dict['mix_color'] = "TGY"
    # #context_dict['mix_states'] = mix.states.all()
    # context = RequestContext(request)
    #
    # return render_to_response('mix_edit.html', context_dict, context)

@login_required
def bird_detail(request, bird_name_slug):
    context_dict = {}
    bird = UserBird.objects.filter(user=request.user).get(bird__slug=bird_name_slug)
    context_dict['bird_name'] = bird.bird.name
    context_dict['bird_call'] = bird.bird.bird_call
    context_dict['bird_type'] = bird.bird.bird_type
    if bird.favorite:
        context_dict['favorite'] = "checked=checked"
    if bird.favorite:
        context_dict['excluded'] = "checked=checked"
    context_dict['bird_pile'] = bird.bird_pile
    context_dict['parent_mixes'] = bird.parent_mixes
    context = RequestContext(request)

    return render_to_response('bird_detail.html', context_dict, context)


@csrf_exempt
def ajax(request):
    if request.method == "POST":
        bird = Bird()
        #bird.user = User.objects.all()[0]
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