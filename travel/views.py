import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
import random
from django.core import serializers


from .models import User, Tag, Trip, List, Photo

def index(request):           
    return render(request, "travel/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "travel/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "travel/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        image = request.FILES["prof_pic"]
        home = request.POST["home"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "travel/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.profpic = image
            user.home = home
            user.save()
            wishlist = List.objects.create(lists='Wishlist', user=user)
            wishlist.save()
            pastlist = List.objects.create(lists="Past Trips", user=user)
            pastlist.save()
        except IntegrityError:
            return render(request, "travel/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "travel/register.html")

@login_required
def plan(request):
    if request.method == "POST":
        # get data from form
        user = request.user
        status = request.POST["status"]
        title = request.POST["title"]
        timestamp = timezone.now().strftime("%b %-d, %Y")
        location = request.POST["location"]
        budget = request.POST["budget"]
        plans = request.POST["plans"]
        image = request.FILES["image"]
        tags = request.POST.getlist("tags[]")
        photos = request.FILES.getlist("photos[]")
        # save the trip
        trip = Trip(
                user=user, 
                title=title, 
                budget=budget,
                timestamp=timestamp, 
                plans=plans,
                location=location,
                status=status,
                img=image) 
        trip.save()
        # add to Past Trips list if been
        if status == 'been':
            list_name = List.objects.get(lists='Past Trips', user=user)
            list_name.trips.add(trip)
        # save the tags
        for i in range(len(tags)):
            tag = Tag.objects.filter(tags=tags[i])
            if tag.exists():
                tag[0].trips.add(trip)
            else:
                tag_name = tags[i]
                if tag_name.strip() != "":
                    new_tag = Tag(
                        tags=tag_name
                        )
                    new_tag.save()
                    new_tag.trips.add(trip)
        # save the photos
        for photo in photos:
            new_photo = Photo.objects.create(photos=photo, trips=trip)
            new_photo.save()
        photos = Photo.objects.filter(trips=trip)
        return render(request, "travel/captions.html", {
            "photos": photos
        })
    else:
        tags = Tag.objects.all().order_by("tags")
        return render(request, "travel/plan.html", {
            "tags": tags
        })

def captions(request):
    photos = request.POST.getlist("photos[]")
    captions = request.POST.getlist("captions[]")
    for i in range(len(photos)):
        photo = Photo.objects.get(id=photos[i])
        photo.caption = captions[i]
        photo.save()
    trips = Trip.objects.all().order_by("-id")
    return render(request, "travel/index.html", {
        "trips": trips
    })



def trip_view(request, trip_id):
    # show details of one trip including all tags
    user = request.user
    trip = Trip.objects.get(id=trip_id)
    trip_tags = []
    all_tags = Tag.objects.all()
    # go through all tags and check if the trip is one with the tag
    for i in range(len(all_tags)):
        tag = all_tags[i]
        if trip in tag.trips.all():
            tag = all_tags[i].tags
            #if it is, add the tag name to the trip tags list
            trip_tags.append(tag)
    trip_lists = []
    all_lists = List.objects.filter(user=user)
    for i in range(len(all_lists)):
        list = all_lists[i]
        if trip not in list.trips.all():
            trip_lists.append(list)
    if Photo.objects.filter(trips=trip).exists():
        photos = Photo.objects.filter(trips=trip)
    else:
        photos = []
    return render(request, "travel/trip.html", {
        "trip": trip,
        "tags": sorted(trip_tags),
        "lists": trip_lists,
        "photos": photos
    })

def profile(request, profile_id):
    user = request.user
    profile = User.objects.get(id=profile_id)
    # display user's lists
    lists = List.objects.filter(user=user)
    trips = Trip.objects.filter(user=profile)
    paginator = Paginator(trips, 10) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "travel/profile.html", {
        "user": user,
        "profile": profile,
        "trips": trips,
        "page_obj": page_obj,
        "lists": lists
    })

def tags(request, tag_name):
    tag = Tag.objects.get(tags=tag_name)
    trips = tag.trips.all()
    paginator = Paginator(trips, 10) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "travel/browse.html", {
        "trips": trips,
        "page_obj": page_obj,
        "message": 'Showing trips with the ' + '<strong class="tag_name">#' + tag_name + '</strong> tag'
    })

def browse(request):
    if request.method == "POST":
        sort_by = request.POST["sort"]
        trips = Trip.objects.all().order_by(sort_by)
    else:
        trips = Trip.objects.all().order_by("-id")
        paginator = Paginator(trips, 10) # Show 10 posts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "travel/browse.html", {
        "trips": trips,
        "page_obj": page_obj
    })

def random_trip(request):
    user = request.user
    trips = Trip.objects.all()
    trip = random.choice(trips)
    trip_tags = []
    all_tags = Tag.objects.all()
    # go through all tags and check if the trip is one with the tag
    for i in range(len(all_tags)):
        tag = all_tags[i]
        if trip in tag.trips.all():
            tag = all_tags[i].tags
            #if it is, add the tag name to the trip tags list
            trip_tags.append(tag)
    trip_lists = []
    all_lists = List.objects.filter(user=user)
    for i in range(len(all_lists)):
        list = all_lists[i]
        if trip not in list.trips.all():
            trip_lists.append(list)
    if Photo.objects.filter(trips=trip).exists():
        photos = Photo.objects.filter(trips=trip)
    else:
        photos = []
    return render(request, "travel/trip.html", {
        "trip": trip,
        "tags": sorted(trip_tags),
        "lists": trip_lists,
        "photos": photos
    })

@login_required
def edit_profile(request):
    user = request.user
    user_id = user.id

    if request.method == "POST":
        # if no name/home/image/list_name then default is False
        name = request.POST.get("name", False)
        home = request.POST.get("home", False)
        image = request.FILES.get("image", False)
        list_name = request.POST.get("list_name", False)
        profile = User.objects.get(id=user_id)
        if list_name:
            new_list = List.objects.create(lists=list_name, user=user)
            new_list.save()
            lists = List.objects.filter(user=user)
            return render(request, "travel/mylists.html", {
                "lists": lists,
                "profile": user
            })
        if image:
            profile.profpic = image
            profile.save()
        if name:
            profile.first_name = name
            profile.save()
        if home:
            profile.home = home
            profile.save()
        return render(request, "travel/profile.html", {
            "profile": profile,
            "user": profile
        })
    else: 
        return render(request, "travel/profile.html", {
            "profile": user,
            "user": user
        })

@login_required
def lists_view(request, list_name):
    user = request.user
    # if user created the trip
    if list_name == 'mine':
        trips = Trip.objects.filter(user=user)
        message = 'Showing trips that <strong class="tag_name">you</strong> created'
        return render(request, "travel/browse.html", {
            "trips": trips,
            "message": message
        })
    # display more lists
    if list_name == 'more':
        lists = List.objects.filter(user=user)
        return render(request, "travel/mylists.html", {
            "lists": lists,
            "profile": user
        })
    # if list name is something else, get all the trips that are on that list
    else: 
        list = List.objects.get(lists=list_name, user=user)
        # if there is at least one trip on the list
        if len(list.trips.all()) != 0:
            trips = list.trips.all()
            message = 'Showing trips from your list: <strong class="tag_name">' + list_name + '</strong>'
            button = True
        # if there are no trips on the list
        else:
            trips = []
            message = "You don't have any trips on the list: <strong class='tag_name'>" + list_name + "</strong>"
            button = False
        paginator = Paginator(trips, 10) # Show 10 posts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "travel/browse.html", {
            "trips": trips,
            "message": message,
            "button": button,
            "list": list_name,
            "page_obj": page_obj
        })

def search(request):
    if request.method == 'POST':
        search_text = request.POST["search"]
        request.session['search'] = search_text
        # search the titles, locations, and plans for the user's query (icontains is case insensitive)
        trips = Trip.objects.filter(title__icontains=search_text) | Trip.objects.filter(location__icontains=search_text) | Trip.objects.filter(plans__icontains=search_text)
        message = 'Search results for <strong class="tag_name">' + search_text + '</strong>'
        if len(trips) == 0:
            message = 'No results for your search <strong class="tag_name"> "'+ search + '"</strong>'
        paginator = Paginator(trips, 10) # Show 10 posts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "travel/browse.html", {
            "trips": trips,
            "message": message,
            "page_obj": page_obj
        })
    if request.method == 'GET':
        if 'search' in request.session:
            search_text = request.session['search']
            trips = Trip.objects.filter(title__icontains=search_text) | Trip.objects.filter(location__icontains=search_text) | Trip.objects.filter(plans__icontains=search_text)
            message = 'Search results for <strong class="tag_name">' + search_text + '</strong>'
            paginator = Paginator(trips, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'travel/browse.html', {
                "page_obj": page_obj,
                "trips": trips,
                "message": message
                })

def searchMap(request, search):
    if request.method == 'POST':
        search_text = search
        request.session['search'] = search_text
        # search the titles, locations, and plans for the user's query (icontains is case insensitive)
        trips = Trip.objects.filter(title__icontains=search_text) | Trip.objects.filter(location__icontains=search_text) | Trip.objects.filter(plans__icontains=search_text)
        message = 'Search results for <strong class="tag_name">' + search_text + '</strong>'
        if len(trips) == 0:
            message = 'No results for your search <strong class="tag_name"> "'+ search + '"</strong>'
        paginator = Paginator(trips, 10) # Show 10 posts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "travel/browse.html", {
            "trips": trips,
            "message": message,
            "page_obj": page_obj
        })
    if request.method == 'GET':
        if 'search' in request.session:
            search_text = request.session['search']
            trips = Trip.objects.filter(title__icontains=search_text) | Trip.objects.filter(location__icontains=search_text) | Trip.objects.filter(plans__icontains=search_text)
            message = 'Search results for <strong class="tag_name">' + search_text + '</strong>'
            paginator = Paginator(trips, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'travel/browse.html', {
                "page_obj": page_obj,
                "trips": trips,
                "message": message
                })

def addToList(request):
    trip_id = request.POST["trip"]
    trip = Trip.objects.get(id=trip_id)
    lists = request.POST.getlist("list[]")
    user = request.user
    for list in lists:
        if list != "":
            if List.objects.filter(user=user, lists=list).exists():
                list = List.objects.get(user=user, lists=list)
                list.trips.add(trip)
            else:
                new_list = List.objects.create(lists=list, user=user)
                new_list.save()
                new_list.trips.add(trip)
    return HttpResponse(status=204)

def removeFromList(request, list_name, trip_id):
    user = request.user
    trip = Trip.objects.get(id=trip_id)
    list = List.objects.get(lists=list_name, user=user)
    list.trips.remove(trip)
    return HttpResponse(status=204)

@login_required
def edit_trip(request, trip_id):
    if request.method == "POST":
        # get data from form
        user = request.user
        status = request.POST["status"]
        title = request.POST["title"]
        timestamp = timezone.now().strftime("%b %-d, %Y")
        plans = request.POST["plans"]
        new_tags = request.POST.getlist("tags[]")
        remove_photos = request.POST.getlist("removePhotos[]")
        new_photos = request.FILES.getlist("newPhotos[]")
        photo_ids = request.POST.getlist("photos[]")
        captions = request.POST.getlist("captions[]")
        
        # save the trip details
        trip = Trip.objects.get(id=trip_id)
        trip.plans = plans
        trip.title = title
        trip.status = status
        trip.timestamp = timestamp
        trip.save()

        # UPDATE STATUS LIST
        # get the past trips list
        been_list = List.objects.get(lists='Past Trips', user=user)
        # get all trips on the past trips lists
        been_trips = been_list.trips.all()
        # if the updated status is been
        if status == 'been':
            # if the trip is not already on the Past Trips list, add it
            if trip not in been_trips:
                been_list.trips.add(trip)
        # if the updated status is future
        if status == 'future':
            # if the trip was previously on the Past Trips list, remove it 
            if trip in been_trips:
                been_list.trips.remove(trip)

        # get all previous tags for trip (trip_tags)
        old_tags = []
        all_tags = Tag.objects.all()
        # go through all tags and check if the trip is one with the tag
        for i in range(len(all_tags)):
            tag = all_tags[i]
            if trip in tag.trips.all():
                tag = all_tags[i].tags
                #if it is, add the tag name to the trip tags list
                old_tags.append(tag)
        
        # go through all new tags, if not on previous tag list, add it  
        for new_tag in new_tags:
            if new_tag not in old_tags:
                tag_name = new_tag
                if tag_name != "":
                    add_tag = Tag(
                        tags=tag_name
                        )
                    add_tag.save()
                    add_tag.trips.add(trip)
        
        # go through all old tags, if not on new tag list, delete it 
        for old_tag in old_tags:
            if old_tag not in new_tags:
                remove_tag = Tag.objects.get(tags=old_tag)
                remove_tag.trips.remove(trip)

        #update photos
        #save new photos
        for photo in new_photos:
            new_photo = Photo.objects.create(photos=photo, trips=trip)
            new_photo.save()
        #save captions
        for i in range(len(captions)):
            photo = Photo.objects.get(id=photo_ids[i])
            photo.caption = captions[i]
            photo.save()
        
        # remove photos on remove list
        for i in range(len(remove_photos)):
            Photo.objects.get(id=remove_photos[i]).delete()

        # render edit page with updated trip details
        trip_tags = []
        all_tags = Tag.objects.all()
        # go through all tags and check if the trip is one with the tag
        for i in range(len(all_tags)):
            tag = all_tags[i]
            if trip in tag.trips.all():
                tag = all_tags[i].tags
                #if it is, add the tag name to the trip tags list
                trip_tags.append(tag)
        if Photo.objects.filter(trips=trip).exists():
            photos = Photo.objects.filter(trips=trip)
        else:
            photos = []
        return render(request, "travel/edit.html", {
            "trip": trip,
            "tags": sorted(trip_tags),
            "photos": photos,
            "message": 'Changes Saved'
        })
    else:
        trip = Trip.objects.get(id=trip_id)
        trip_tags = []
        all_tags = Tag.objects.all()
        # go through all tags and check if the trip is one with the tag
        for i in range(len(all_tags)):
            tag = all_tags[i]
            if trip in tag.trips.all():
                tag = all_tags[i].tags
                #if it is, add the tag name to the trip tags list
                trip_tags.append(tag)
        if Photo.objects.filter(trips=trip).exists():
            photos = Photo.objects.filter(trips=trip)
        else:
            photos = []
        return render(request, "travel/edit.html", {
            "trip": trip,
            "tags": sorted(trip_tags),
            "photos": photos
        })
    
def all_been(request):
    if request.method == "GET":
        trips = Trip.objects.filter(status='been')
        trips = trips.all()
        response = serializers.serialize("json", trips)
        return HttpResponse(response, content_type='application/json')