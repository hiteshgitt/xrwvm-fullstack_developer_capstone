from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
import logging
import json

# Set up logging
logger = logging.getLogger(__name__)

# ------------------------------
# HTML Form Login View
# ------------------------------
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')  # Redirect to homepage
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password.'
            })

    return render(request, 'login.html')  # GET request

# ------------------------------
# JSON API Login View
# ------------------------------
@csrf_exempt  # If you plan to use token-based auth, remove this and use @csrf_protect + token
def login_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({
                    "status": "error",
                    "message": "Username and password are required."
                }, status=400)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    "status": "Authenticated",
                    "userName": username
                })
            else:
                return JsonResponse({
                    "status": "Invalid credentials",
                    "userName": username
                }, status=401)

        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body.")
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.exception("Unexpected error during login API.")
            return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)

# ------------------------------
# Get Cars API
# ------------------------------
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(f"CarMake count: {count}")
    if(count == 0):
        print("No CarMakes found, calling initiate()...")
        try:
            initiate()
            print("initiate() completed successfully")
        except Exception as e:
            print(f"Error in initiate(): {e}")
            return JsonResponse({"error": f"Failed to populate data: {str(e)}"})
    
    car_models = CarModel.objects.select_related('car_make')
    print(f"CarModel count: {car_models.count()}")
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    print(f"Final cars list: {cars}")
    return JsonResponse({"CarModels":cars})

# ------------------------------
# Registration View
# ------------------------------
def registration(request):
    if request.method == "POST":
        # Handle registration logic here
        return JsonResponse({"message": "Registration functionality coming soon"})
    
    return render(request, 'register.html')

# ------------------------------
# Other Views
# ------------------------------
def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

# ------------------------------
# TODO: Future features
# ------------------------------
# def logout_request(request):
#     pass

# def get_dealerships(request):
#     pass
#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

# def get_dealer_reviews(request, dealer_id):
#     pass
def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

# def get_dealer_details(request, dealer_id):
#     pass
def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})
# def add_review(request):
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})
#     pass