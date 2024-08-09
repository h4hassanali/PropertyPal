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
        # Retrieve city and search type from GET parameters
        city_name = request.GET.get('city_name')
        search_type = request.GET.get('searchType')

        # Validate city and search type
        if not city_name or not search_type:
            return HttpResponse("City name and search type are required")

        try:
            city = City.objects.get(city_name=city_name)
        except City.DoesNotExist:
            return HttpResponse("City not found")

        # Retrieve sort option, default to 'newest' if not provided
        sort_option = request.GET.get('sort', 'newest')

        # Prepare filters based on the search type
        filters = {'city': city}
        if search_type == 'room':
            # Add additional filters if provided
            if request.GET.get('rent_min'):
                filters['rent__gte'] = request.GET.get('rent_min')
            if request.GET.get('rent_max'):
                filters['rent__lte'] = request.GET.get('rent_max')
            if request.GET.get('bills_included'):
                filters['bills_included'] = True
            if request.GET.get('for_female'):
                filters['for_female'] = True
            if request.GET.get('adjusted_with_age_min'):
                filters['adjusted_with_age_min__gte'] = request.GET.get('adjusted_with_age_min')
            if request.GET.get('adjusted_with_age_max'):
                filters['adjusted_with_age_max__lte'] = request.GET.get('adjusted_with_age_max')
            if request.GET.get('room_size'):
                filters['room_size'] = request.GET.get('room_size')
            if request.GET.get('num_of_rooms'):
                filters['num_of_rooms__gte'] = request.GET.get('num_of_rooms')
            if request.GET.get('smoking_allowed'):
                filters['smoking_allowed'] = True
            if request.GET.get('length_of_stay_min'):
                filters['length_of_stay_min__gte'] = request.GET.get('length_of_stay_min')
            if request.GET.get('length_of_stay_max'):
                filters['length_of_stay_max__lte'] = request.GET.get('length_of_stay_max')
            if request.GET.get('free_wifi'):
                filters['free_wifi'] = True

            items = Room.objects.filter(**filters).order_by(
                'rent' if sort_option == 'price_low_to_high' else 
                '-rent' if sort_option == 'price_high_to_low' else 
                '-id' if sort_option == 'newest' else 'id'
            )
            attachments = Attachment.objects.filter(room__in=items)

        elif search_type == 'roommate':
            if request.GET.get('budget_min'):
                filters['budget__gte'] = request.GET.get('budget_min')
            if request.GET.get('budget_max'):
                filters['budget__lte'] = request.GET.get('budget_max')
            if request.GET.get('occupation'):
                filters['occupation'] = request.GET.get('occupation')
            if request.GET.get('gender'):
                filters['gender'] = request.GET.get('gender')
            if request.GET.get('music_allowed'):
                filters['music'] = request.GET.get('music_allowed')
            if request.GET.get('smoking_allowed'):
                filters['smoking_allowed'] = True
            if request.GET.get('free_wifi'):
                filters['free_wifi'] = True

            items = RoommateProfile.objects.filter(**filters).order_by(
                'budget' if sort_option == 'price_low_to_high' else 
                '-budget' if sort_option == 'price_high_to_low' else 
                '-id' if sort_option == 'newest' else 'id'
            )
            attachments = Attachment.objects.filter(roommate_profile__in=items)

        else:  # accessory
            if request.GET.get('price_min'):
                filters['price__gte'] = request.GET.get('price_min')
            if request.GET.get('price_max'):
                filters['price__lte'] = request.GET.get('price_max')

            items = Accessory.objects.filter(**filters).order_by(
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
def advanced_search_result(request):
    if request.method == "GET":
        city_name = request.GET.get('city_name')
        search_type = request.GET.get('searchType')

        # Ensure city name and search type are provided
        if not city_name or search_type not in ['room', 'roommate', 'accessory']:
            return HttpResponse("Invalid input", status=400)

        try:
            city = City.objects.get(city_name=city_name)
        except City.DoesNotExist:
            return HttpResponse("City not found", status=404)

        # Initialize result set based on search type
        items = None

        if search_type == 'room':
            items = Room.objects.filter(city=city)

            # Apply additional filters
            rent_min = request.GET.get('rent_min')
            rent_max = request.GET.get('rent_max')
            if rent_min:
                items = items.filter(rent__gte=rent_min)
            if rent_max:
                items = items.filter(rent__lte=rent_max)

            bills_included = request.GET.get('bills_included')
            if bills_included:
                items = items.filter(bills_included=bills_included == 'True')

            for_female = request.GET.get('for_female')
            if for_female:
                items = items.filter(for_female=for_female == 'True')

            room_size = request.GET.get('room_size')
            if room_size:
                items = items.filter(room_size=room_size)

            num_of_rooms = request.GET.get('num_of_rooms')
            if num_of_rooms:
                items = items.filter(num_of_rooms=num_of_rooms)

            smoking_allowed = request.GET.get('smoking_allowed')
            if smoking_allowed:
                items = items.filter(smoking_allowed=smoking_allowed == 'True')

            length_of_stay_min = request.GET.get('length_of_stay_min')
            length_of_stay_max = request.GET.get('length_of_stay_max')
            if length_of_stay_min:
                items = items.filter(length_of_stay_min__gte=length_of_stay_min)
            if length_of_stay_max:
                items = items.filter(length_of_stay_max__lte=length_of_stay_max)

            move_on_timing = request.GET.get('move_on_timing')
            if move_on_timing:
                items = items.filter(move_on_timing=move_on_timing)

            free_wifi = request.GET.get('free_wifi')
            if free_wifi:
                items = items.filter(free_wifi=free_wifi == 'True')

            # Fetch attachments for rooms
            attachments = Attachment.objects.filter(room__in=items)

        elif search_type == 'roommate':
            items = RoommateProfile.objects.filter(city=city)

            # Apply additional filters
            occupation = request.GET.get('occupation')
            if occupation:
                items = items.filter(occupation=occupation)

            gender = request.GET.get('gender')
            if gender:
                items = items.filter(gender=gender)

            music_allowed = request.GET.get('music_allowed')
            if music_allowed:
                items = items.filter(music=music_allowed)

            adjusted_with_age_min = request.GET.get('adjusted_with_age_min')
            adjusted_with_age_max = request.GET.get('adjusted_with_age_max')
            if adjusted_with_age_min:
                items = items.filter(adjusted_with_age_min__gte=adjusted_with_age_min)
            if adjusted_with_age_max:
                items = items.filter(adjusted_with_age_max__lte=adjusted_with_age_max)

            smoking_allowed = request.GET.get('smoking_allowed')
            if smoking_allowed:
                items = items.filter(smoking_allowed=smoking_allowed == 'True')

            bills_included = request.GET.get('bills_included')
            if bills_included:
                items = items.filter(bills_included=bills_included == 'True')

            free_wifi = request.GET.get('free_wifi')
            if free_wifi:
                items = items.filter(free_wifi=free_wifi == 'True')

            # Fetch attachments for roommate profiles
            attachments = Attachment.objects.filter(roommate_profile__in=items)

        elif search_type == 'accessory':
            items = Accessory.objects.filter(city=city)

            # Apply additional filters
            price_min = request.GET.get('price_min')
            price_max = request.GET.get('price_max')
            if price_min:
                items = items.filter(price__gte=price_min)
            if price_max:
                items = items.filter(price__lte=price_max)

            # Fetch attachments for accessories
            attachments = Attachment.objects.filter(accessory__in=items)

        else:
            return HttpResponse("Invalid search type", status=400)

        # Prepare context
        context = {
            'items': items,
            'attachments': attachments,
            'city_name': city_name,
            'search_type': search_type,
        }

        # Render the template with context
        return render(request, 'advanced_search_result.html', context)
    if request.method == "GET":
        # Retrieve the values from the form using request.GET
        city_name = request.GET.get('city_name')
        search_type = request.GET.get('searchType')

        # Ensure city name and search type are provided
        if not city_name or not search_type:
            return HttpResponse("City name and search type are required.", status=400)

        # Filter city by name
        try:
            city = City.objects.get(city_name=city_name)
        except City.DoesNotExist:
            return HttpResponse("City not found.", status=404)

        # Initialize empty result set
        results = None

        # Filter based on search type
        if search_type == 'room':
            results = Room.objects.filter(city=city)

            # Apply additional filters if provided
            rent_min = request.GET.get('rent_min')
            rent_max = request.GET.get('rent_max')
            if rent_min:
                results = results.filter(rent__gte=rent_min)
            if rent_max:
                results = results.filter(rent__lte=rent_max)

            bills_included = request.GET.get('bills_included')
            if bills_included:
                results = results.filter(bills_included=bills_included == 'True')

            for_female = request.GET.get('for_female')
            if for_female:
                results = results.filter(for_female=for_female == 'True')

            adjusted_with_age_min = request.GET.get('adjusted_with_age_min')
            adjusted_with_age_max = request.GET.get('adjusted_with_age_max')
            if adjusted_with_age_min:
                results = results.filter(adjusted_with_age_min__gte=adjusted_with_age_min)
            if adjusted_with_age_max:
                results = results.filter(adjusted_with_age_max__lte=adjusted_with_age_max)

            room_size = request.GET.get('room_size')
            if room_size:
                results = results.filter(room_size=room_size)

            num_of_rooms = request.GET.get('num_of_rooms')
            if num_of_rooms:
                results = results.filter(num_of_rooms=num_of_rooms)

            smoking_allowed = request.GET.get('smoking_allowed')
            if smoking_allowed:
                results = results.filter(smoking_allowed=smoking_allowed == 'True')

            length_of_stay_min = request.GET.get('length_of_stay_min')
            length_of_stay_max = request.GET.get('length_of_stay_max')
            if length_of_stay_min:
                results = results.filter(length_of_stay_min__gte=length_of_stay_min)
            if length_of_stay_max:
                results = results.filter(length_of_stay_max__lte=length_of_stay_max)

            move_on_timing = request.GET.get('move_on_timing')
            if move_on_timing:
                results = results.filter(move_on_timing=move_on_timing)

            free_wifi = request.GET.get('free_wifi')
            if free_wifi:
                results = results.filter(free_wifi=free_wifi == 'True')

        elif search_type == 'roommate':
            results = RoommateProfile.objects.filter(city=city)

            # Apply additional filters if provided
            occupation = request.GET.get('occupation')
            if occupation:
                results = results.filter(occupation=occupation)

            gender = request.GET.get('gender')
            if gender:
                results = results.filter(gender=gender)

            music_allowed = request.GET.get('music_allowed')
            if music_allowed:
                results = results.filter(music=music_allowed)

            adjusted_with_age_min = request.GET.get('adjusted_with_age_min')
            adjusted_with_age_max = request.GET.get('adjusted_with_age_max')
            if adjusted_with_age_min:
                results = results.filter(adjusted_with_age_min__gte=adjusted_with_age_min)
            if adjusted_with_age_max:
                results = results.filter(adjusted_with_age_max__lte=adjusted_with_age_max)

            smoking_allowed = request.GET.get('smoking_allowed')
            if smoking_allowed:
                results = results.filter(smoking_allowed=smoking_allowed == 'True')

            bills_included = request.GET.get('bills_included')
            if bills_included:
                results = results.filter(bills_included=bills_included == 'True')

            free_wifi = request.GET.get('free_wifi')
            if free_wifi:
                results = results.filter(free_wifi=free_wifi == 'True')

        elif search_type == 'accessory':
            results = Accessory.objects.filter(city=city)

            # Apply additional filters if provided
            price_min = request.GET.get('price_min')
            price_max = request.GET.get('price_max')
            if price_min:
                results = results.filter(price__gte=price_min)
            if price_max:
                results = results.filter(price__lte=price_max)

        else:
            return HttpResponse("Invalid search type.", status=400)

        # Prepare the response to display filtered results
        if results is not None:
            response = "\n".join([str(result) for result in results])
            return HttpResponse(response.replace('\n', '<br>'))
        else:
            return HttpResponse("No results found.")