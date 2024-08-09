from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import City, Room, RoommateProfile, Accessory, Attachment
import random

def index(request):
    return render(request, 'index.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def search(request):
    if request.method == "POST":
        city_name = request.POST.get('city_name')
        search_type = request.POST.get('searchType')
        sort_option = request.POST.get('sort', 'price_low_to_high')
    elif request.method == "GET":
        city_name = request.GET.get('city_name')
        search_type = request.GET.get('searchType')
        sort_option = request.GET.get('sort', 'price_low_to_high')
    else:
        return HttpResponse("Invalid request method")

    # Validate input
    if not city_name or search_type not in ['room', 'roommate', 'accessory']:
        return HttpResponse("Invalid input")

    try:
        city = City.objects.get(city_name=city_name)
    except City.DoesNotExist:
        return HttpResponse("City not found")

    if search_type == 'room':
        if sort_option == 'price_low_to_high':
            items = Room.objects.filter(city=city).order_by('rent')
        elif sort_option == 'price_high_to_low':
            items = Room.objects.filter(city=city).order_by('-rent')
        elif sort_option == 'newest':
            items = Room.objects.filter(city=city).order_by('-id')  # Assuming 'id' corresponds to the creation order
        elif sort_option == 'oldest':
            items = Room.objects.filter(city=city).order_by('id')  # Assuming 'id' corresponds to the creation order
        else:
            items = Room.objects.filter(city=city)
        
        # Fetch attachments for rooms
        attachments = Attachment.objects.filter(room__in=items)
        
        context = {
            'items': items,
            'attachments': attachments,
            'city_name': city_name,
            'search_type': 'room',
            'sort_option': sort_option
        }
        return render(request, 'search_result_ui.html', context)
    
    elif search_type == 'roommate':
        if sort_option == 'price_low_to_high':
            items = RoommateProfile.objects.filter(city=city).order_by('budget')
        elif sort_option == 'price_high_to_low':
            items = RoommateProfile.objects.filter(city=city).order_by('-budget')
        elif sort_option == 'newest':
            items = RoommateProfile.objects.filter(city=city).order_by('-id')  # Assuming 'id' corresponds to the creation order
        elif sort_option == 'oldest':
            items = RoommateProfile.objects.filter(city=city).order_by('id')  # Assuming 'id' corresponds to the creation order
        else:
            items = RoommateProfile.objects.filter(city=city)
        
        # Fetch attachments for roommate profiles
        attachments = Attachment.objects.filter(roommate_profile__in=items)
        
        context = {
            'items': items,
            'attachments': attachments,
            'city_name': city_name,
            'search_type': 'roommate',
            'sort_option': sort_option
        }
        return render(request, 'search_result_ui.html', context)
    
    elif search_type == 'accessory':
        if sort_option == 'price_low_to_high':
            items = Accessory.objects.filter(city=city).order_by('price')
        elif sort_option == 'price_high_to_low':
            items = Accessory.objects.filter(city=city).order_by('-price')
        elif sort_option == 'newest':
            items = Accessory.objects.filter(city=city).order_by('-id')  # Assuming 'id' corresponds to the creation order
        elif sort_option == 'oldest':
            items = Accessory.objects.filter(city=city).order_by('id')  # Assuming 'id' corresponds to the creation order
        else:
            items = Accessory.objects.filter(city=city)
        
        # Fetch attachments for accessories
        attachments = Attachment.objects.filter(accessory__in=items)
        
        context = {
            'items': items,
            'attachments': attachments,
            'city_name': city_name,
            'search_type': 'accessory',
            'sort_option': sort_option
        }
        return render(request, 'search_result_ui.html', context)

    else:
        return HttpResponse("Invalid search type")

def autocomplete(request):
    if 'term' in request.GET:
        qs = City.objects.filter(city_name__icontains=request.GET.get('term'))
        cities = list(qs.values_list('city_name', flat=True))
        return JsonResponse(cities, safe=False)
    return JsonResponse([], safe=False)

def list_accessories(request):
    accessories = Accessory.objects.all()
    context = {
        'accessories': accessories
    }
    return render(request, 'accessory_list.html', context)


def advanced_search(request):
    if request.method == "GET":
        # Retrieve city and search type from GET parameters or generate random ones
        city_name = request.GET.get('city_name')
        search_type = request.GET.get('searchType')

        if not city_name:
            city = City.objects.order_by('?').first()
            city_name = city.city_name
        else:
            city = City.objects.get(city_name=city_name)
        
        if not search_type:
            search_type = random.choice(['room', 'roommate', 'accessory'])

        # Retrieve sort option, default to 'newest' if not provided
        sort_option = request.GET.get('sort', 'newest')

        # Fetch items based on search type
        if search_type == 'room':
            items = Room.objects.filter(city=city).order_by(
                'rent' if sort_option == 'price_low_to_high' else 
                '-rent' if sort_option == 'price_high_to_low' else 
                '-id' if sort_option == 'newest' else 'id'
            )
            attachments = Attachment.objects.filter(room__in=items)
        elif search_type == 'roommate':
            items = RoommateProfile.objects.filter(city=city).order_by(
                'budget' if sort_option == 'price_low_to_high' else 
                '-budget' if sort_option == 'price_high_to_low' else 
                '-id' if sort_option == 'newest' else 'id'
            )
            attachments = Attachment.objects.filter(roommate_profile__in=items)
        else:  # accessory
            items = Accessory.objects.filter(city=city).order_by(
                'price' if sort_option == 'price_low_to_high' else 
                '-price' if sort_option == 'price_high_to_low' else 
                '-id' if sort_option == 'newest' else 'id'
            )
            attachments = Attachment.objects.filter(accessory__in=items)

        # Prepare context data
        context = {
            'items': items,
            'attachments': attachments,
            'city_name': city_name,
            'search_type': search_type,
            'sort_option': sort_option
        }

        # Pass data to the advanced_search_ui.html page
        return render(request, 'advanced_search_ui.html', context)

    else:
        return HttpResponse("POST request not allowed for this action")






# def advanced_search_home(request):
#     return render(request,'advanced_search.html')

# def advanced_search(request):
#     if request.method == "POST":
#         city_name = request.POST.get('city_name')
#         search_type = request.POST.get('searchType')
#         sort_option = request.POST.get('sort', 'price_low_to_high')
#     elif request.method == "GET":
#         city_name = request.GET.get('city_name')
#         search_type = request.GET.get('searchType')
#         sort_option = request.GET.get('sort', 'price_low_to_high')
#     else:
#         return HttpResponse("Invalid request method")

#     # Validate input
#     if not city_name or search_type not in ['room', 'roommate', 'accessory']:
#         return HttpResponse("Invalid input")

#     try:
#         city = City.objects.get(city_name=city_name)
#     except City.DoesNotExist:
#         return HttpResponse("City not found")

#     if search_type == 'room':
#         if sort_option == 'price_low_to_high':
#             items = Room.objects.filter(city=city).order_by('rent')
#         elif sort_option == 'price_high_to_low':
#             items = Room.objects.filter(city=city).order_by('-rent')
#         elif sort_option == 'newest':
#             items = Room.objects.filter(city=city).order_by('-id')  # Assuming 'id' corresponds to the creation order
#         elif sort_option == 'oldest':
#             items = Room.objects.filter(city=city).order_by('id')  # Assuming 'id' corresponds to the creation order
#         else:
#             items = Room.objects.filter(city=city)
        
#         # Fetch attachments for rooms
#         attachments = Attachment.objects.filter(room__in=items)
        
#         context = {
#             'items': items,
#             'attachments': attachments,
#             'city_name': city_name,
#             'search_type': 'room',
#             'sort_option': sort_option
#         }
#         return render(request, 'search_result_ui.html', context)
    
#     elif search_type == 'roommate':
#         if sort_option == 'price_low_to_high':
#             items = RoommateProfile.objects.filter(city=city).order_by('budget')
#         elif sort_option == 'price_high_to_low':
#             items = RoommateProfile.objects.filter(city=city).order_by('-budget')
#         elif sort_option == 'newest':
#             items = RoommateProfile.objects.filter(city=city).order_by('-id')  # Assuming 'id' corresponds to the creation order
#         elif sort_option == 'oldest':
#             items = RoommateProfile.objects.filter(city=city).order_by('id')  # Assuming 'id' corresponds to the creation order
#         else:
#             items = RoommateProfile.objects.filter(city=city)
        
#         # Fetch attachments for roommate profiles
#         attachments = Attachment.objects.filter(roommate_profile__in=items)
        
#         context = {
#             'items': items,
#             'attachments': attachments,
#             'city_name': city_name,
#             'search_type': 'roommate',
#             'sort_option': sort_option
#         }
#         return render(request, 'search_result_ui.html', context)
    
#     elif search_type == 'accessory':
#         if sort_option == 'price_low_to_high':
#             items = Accessory.objects.filter(city=city).order_by('price')
#         elif sort_option == 'price_high_to_low':
#             items = Accessory.objects.filter(city=city).order_by('-price')
#         elif sort_option == 'newest':
#             items = Accessory.objects.filter(city=city).order_by('-id')  # Assuming 'id' corresponds to the creation order
#         elif sort_option == 'oldest':
#             items = Accessory.objects.filter(city=city).order_by('id')  # Assuming 'id' corresponds to the creation order
#         else:
#             items = Accessory.objects.filter(city=city)
        
#         # Fetch attachments for accessories
#         attachments = Attachment.objects.filter(accessory__in=items)
        
#         context = {
#             'items': items,
#             'attachments': attachments,
#             'city_name': city_name,
#             'search_type': 'accessory',
#             'sort_option': sort_option
#         }
#         return render(request, 'search_result_ui.html', context)

#     else:
#         return HttpResponse("Invalid search type")