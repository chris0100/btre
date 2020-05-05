from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage,PageNotAnInteger,Page,Paginator
from .models import Listing
from listings.choices import price_choices, bedroom_choices, state_choices

# Create your views here.


def index(request):
    #los ordena por fecha y solo muestra los que estan publicados(true)
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings':paged_listings
    }

    return render(request, 'listings/listings.html',context)



def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing' : listing
    }
    return render(request, 'listings/listing.html',context)





def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    print('empieza la busqueda: ' + str(queryset_list))

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        print(str(city))
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
            print('ingresa en la busqueda: ' + str(queryset_list))

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        print('sera que ingresa aca?')
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    #keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)


    context = {
        'state_choices' : state_choices,
        'bedroom_choices' : bedroom_choices,
        'price_choices' : price_choices,
        'listings': queryset_list,
        'values' : request.GET
    }
    return render(request, 'listings/search.html', context)