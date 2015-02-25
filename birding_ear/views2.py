from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from .models import Bird, State, BirdType, UserBird, Mix, Drill
from json import dumps, loads
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def register(request):
    context_dict = {}
    context_dict['username_taken'] = False
    context_dict['submitted'] = False
    if request.method == "POST":
        # check to see if username already exists. Return error.
        users = User.objects.filter(username=request.POST["username"])
        print request.POST["username"]
        print users
        if len(users) > 0: #test for existence of user
            print "taken"
            context_dict['username_taken'] = True
            context_dict['username_input'] = request.POST["username"]
        else:
            print "not taken"
            user = User.objects.create_user(request.POST["username"], None, request.POST["password"])
            context_dict['submitted'] = True
            #extend the bird model
            for b in Bird.objects.all():
                ub = UserBird()
                ub.bird = b
                ub.user = user
                ub.save()
            #create drill settings
            drill = Drill()
            drill.user = user
            drill.save()
            user.save()
            loginuser = auth.authenticate(username=request.POST["username"], password=request.POST["password"])

            auth.login(request, loginuser)
            return redirect('index')
    context = RequestContext(request)
    return render_to_response('register.html', context_dict, context)


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
    fav_learned = UserBird.objects.filter(user=request.user).filter(favorite=True).filter(bird_pile='L')
    fav_total = UserBird.objects.filter(user=request.user).filter(favorite=True)
    context_dict = {'mixes': mix_list, 'fav_learned': fav_learned, 'fav_total': fav_total}
    context = RequestContext(request)

    # Render the response and send it back!
    return render_to_response('index.html', context_dict, context)


@login_required
def mix_detail(request, mix_id_slug):
    context_dict = {}
    mix = Mix.objects.filter(user=request.user).get(slug=mix_id_slug)
    context_dict['mix_slug'] = mix_id_slug
    context_dict['mix_nickname'] = mix.nickname
    context_dict['mix_description'] = mix.description
    context_dict['mix_color'] = mix.color
    context_dict['mix_states'] = mix.states.all().order_by("name")
    context_dict['mix_bird_types'] = mix.bird_types.all()
    context_dict['bird_list'] = mix.bird_list
    context_dict['num_learned'] = mix.num_learned
    context = RequestContext(request)
    return render_to_response('mix_detail.html', context_dict, context)


@login_required
def mix_settings_edit(request, mix_id_slug):
    context_dict = {}
    mix = Mix.objects.filter(user=request.user).get(slug=mix_id_slug)
    if request.method == "POST":
        if request.POST["action"] == "delete":
            mix.delete()
            return redirect('/')
        else:
            mix.nickname = request.POST["nickname"]
            mix.description = request.POST["description"]
            mix.color = request.POST["color"]
            mix.states = request.POST.getlist('states')
            mix.bird_types = request.POST.getlist('bird_types')
            mix.user = request.user
            mix.save()
            mix_id_slug = mix.slug
            return redirect('/mix_detail/' + mix_id_slug)
    else:
        bird_type_list = BirdType.objects.all()
        mix_bird_types = mix.bird_types.all()
        state_list = State.objects.all().order_by("name")
        mix_states = mix.states.all()
        #shows selected bird_types checked
        for bird_type in bird_type_list:
            if bird_type in mix_bird_types:
                bird_type.selected = True
        #shows selected states checked
        for state in state_list:
            if state in mix_states:
                state.selected = True
        context_dict['bird_type_list'] = bird_type_list
        context_dict['state_list'] = state_list
        context_dict['mix_nickname'] = mix.nickname
        context_dict['mix_description'] = mix.description
        context_dict['mix_color'] = mix.color
        context_dict['mix_slug'] = mix.slug
        context_dict['mix_id'] = mix.id

        context = RequestContext(request)
        return render_to_response('mix_edit.html', context_dict, context)


@login_required
def settings(request):
    context_dict = {}
    drill_setting = Drill.objects.get(user=request.user)
    if request.method == "POST":
        if request.POST["action"] == "reset":
            drill_setting.frequency_new = 3
            drill_setting.frequency_learned = 2
            drill_setting.frequency_missed = 4
        else:
            #if request.POST["action"] === "delete" ... drill_setting.user = request.user
            #drill_setting.delete()
            #else...
            drill_setting.frequency_new = request.POST["frequency_new"]
            drill_setting.frequency_learned = request.POST["frequency_learned"]
            drill_setting.frequency_missed = request.POST["frequency_missed"]
            # drill_setting.batch_size = request.POST["batch_size"]
            # drill_setting.next_batch = request.POST["next_batch"]
            # #updates if "Skip audio for answer options" is checked
            # if "challenge_level" in request.POST:
            #     drill_setting.challenge_level = True
            # else:
            #     drill_setting.challenge_level = False
            # #updates if "Group related birds together" is checked
            # if "drill_order" in request.POST:
            #     drill_setting.challenge_level = "REL"
            # else:
            #     drill_setting.challenge_level = "RAN"
            drill_setting.user = request.user
            drill_setting.save()
    context_dict['frequency_new'] = drill_setting.frequency_new
    context_dict['frequency_learned'] = drill_setting.frequency_learned
    context_dict['frequency_missed'] = drill_setting.frequency_missed
        # context_dict['batch_size'] = drill_setting.batch_size
        # context_dict['next_batch'] = drill_setting.next_batch
        # #Shows checked if "Skip audio for answer options" is selected
        # if drill_setting.challenge_level:
        #     context_dict['challenge_level'] = "checked"
        # else:
        #     context_dict['challenge_level'] = ""
        # #Shows checked if "Group related birds together" is selected
        # if drill_setting.drill_order == "REL":
        #     context_dict['drill_order'] = "checked"
        # else:
        #     context_dict['drill_order'] = ""
    context = RequestContext(request)
    return render_to_response('settings.html', context_dict, context)


@login_required
def mix_settings_new(request):
    mix = Mix()
    if request.method == "POST":
        mix.user = request.user
        mix.nickname = request.POST["nickname"]
        mix.description = request.POST["description"]
        mix.color = request.POST["color"]
        mix.save()
        mix.states = request.POST.getlist('states')
        mix.bird_types = request.POST.getlist('bird_types')
        mix.save()
        mix_id_slug = mix.slug
        return redirect('/mix_detail/' + mix_id_slug)
    else:
        context_dict = {}
        context_dict['mix_color'] = "TGY"
        context_dict['state_list'] = State.objects.all()
        context_dict['bird_type_list'] = BirdType.objects.all()
        context = RequestContext(request)
        return render_to_response('mix_edit.html', context_dict, context)

@login_required
def bird_detail(request, bird_name_slug):
    context_dict = {}
    bird = UserBird.objects.filter(user=request.user).get(bird__slug=bird_name_slug)
    context_dict['bird_id'] = bird.id
    context_dict['bird_name'] = bird.bird.name
    context_dict['bird_call'] = bird.bird.bird_call
    context_dict['bird_type'] = bird.bird.bird_type
    if bird.favorite:
        context_dict['favorite'] = "checked"
    else:
        context_dict['favorite'] = ""
    if bird.excluded:
        context_dict['excluded'] = "checked"
    else:
        context_dict['excluded'] = ""
    context_dict['bird_pile'] = bird.bird_pile
    context_dict['parent_mixes'] = bird.parent_mixes
    context = RequestContext(request)

    return render_to_response('bird_detail.html', context_dict, context)

@csrf_exempt
def update_bird_detail(request):
    if request.method == "POST":
        b_id = request.POST["bid"]
        if request.POST["favorite"] == "true":
            b_favorite = True
        else:
            b_favorite = False
        if request.POST["excluded"] == "true":
            b_excluded = True
        else:
            b_excluded = False
        bird = UserBird.objects.filter(user=request.user).get(bird__id=b_id)
        bird.favorite = b_favorite
        bird.excluded = b_excluded
        bird.save()
    return HttpResponse('{"status":"success"}', content_type="application/json")

@login_required
def favorites(request):
    fav_learned = UserBird.objects.filter(user=request.user).filter(favorite=True).filter(bird_pile='L')
    fav_total = UserBird.objects.filter(user=request.user).filter(favorite=True)
    context_dict = {'fav_learned': fav_learned, 'fav_total': fav_total}
    context = RequestContext(request)
    return render_to_response('favorites.html', context_dict, context)


@csrf_exempt
def drill(request, mix_id_slug):
    #if request.method == "POST":
        #checkAnswer()
    context_dict = {}
    #get birds and details for the relevant mix
    mix = Mix.objects.filter(user=request.user).get(slug=mix_id_slug)
    context_dict['mix_slug'] = mix_id_slug
    context_dict['mix_nickname'] = mix.nickname
    context_dict['mix_color'] = mix.color
    drill_setting = Drill.objects.get(user=request.user)
    context_dict['frequency_new'] = drill_setting.frequency_new
    context_dict['frequency_learned'] = drill_setting.frequency_learned
    context_dict['frequency_missed'] = drill_setting.frequency_missed
    context = RequestContext(request)
    return render_to_response('drill.html', context_dict, context)

@csrf_exempt
def quiz(request, mix_id_slug):
    #if request.method == "POST":
        #checkAnswer()
    context_dict = {}
    #get birds and details for the relevant mix
    mix = Mix.objects.filter(user=request.user).get(slug=mix_id_slug)
    context_dict['mix_slug'] = mix_id_slug
    context_dict['mix_nickname'] = mix.nickname
    context_dict['mix_color'] = mix.color
    context_dict['bird_list'] = mix.bird_list
    context = RequestContext(request)
    return render_to_response('quiz.html', context_dict, context)

@csrf_exempt
def mix_drill_birds(request, mix_id_slug):
    mix = Mix.objects.filter(user=request.user).get(slug=mix_id_slug)
    birds_ajax = list(mix.bird_list())
    birds_ajax_list = []
    for b in birds_ajax:
        birds_ajax_list.append({
            "bird_pile": b.bird_pile,
            "bird_narration": b.bird.narration,
            "bird_call": b.bird.bird_call,
            "name": b.bird.name,
            "bird_type": b.bird.bird_type.name,
            "excluded": b.excluded,
            "id": b.id,
            "bid": b.bird.id
        })

    return HttpResponse(dumps(birds_ajax_list), content_type="application/json")

@csrf_exempt
def update_birdpile(request):
    if request.method == "POST":
        b_id = request.POST["bid"]
        b_birdpile = request.POST["birdpile"]
        bird = UserBird.objects.filter(user=request.user).get(bird__id=b_id)
        bird.bird_pile = b_birdpile
        bird.save()
    return HttpResponse('{"status":"success"}', content_type="application/json")

@csrf_exempt
def ajax(request):
    if request.method == "POST":
        bird = Bird()
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