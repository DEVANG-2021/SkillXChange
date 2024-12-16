from django.shortcuts import render, redirect, HttpResponseRedirect,get_object_or_404
from store.models.product import Products
# from store.models.category import Category
from store.models.connection import ConnectionRequest
from store.models.notifications import Notification
from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from store.models.customer import Customer, Skill  # Import your Customer and Skill models
from store.models.customer_ratings import CustomerRating
import json
from django.db import models
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def rate_customer(request):
    if request.session.get('customer'):
        if request.method == 'POST':
            rater_id = request.session.get('customer')
            
            data = json.loads(request.body)
            rated_customer_id = data.get('rated_customer_id')
            stars = data.get('stars')
            comment = data.get('comment', '')

            if stars < 0 or stars > 5:
                return JsonResponse({'error': 'Stars must be between 0 and 5.'}, status=400)

            rater = get_object_or_404(Customer, id=rater_id)
            rated_customer = get_object_or_404(Customer, id=rated_customer_id)

            # Save the rating
            rating = CustomerRating.objects.create(
                rater=rater,
                rated_customer=rated_customer,
                stars=stars,
                comment=comment
            )

            # Send email to the rated customer
            send_mail(
                subject="You've received a new rating!",
                message=f"Your connection {rater.first_name} has rated your profile {stars} stars with the comment: '{comment}'",
                from_email='devangparmar459@gmail.com',
                recipient_list=[rated_customer.email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Rating submitted successfully.'})

        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        returnUrl = request.META['PATH_INFO']
        return redirect(f'/login?return_url={returnUrl}')

# Function to calculate average rating
def get_average_rating(customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    ratings = CustomerRating.objects.filter(rated_customer=customer)
    if ratings.exists():
        average = ratings.aggregate(models.Avg('stars'))['stars__avg']
        return round(average, 2)  # Rounded to 2 decimal points
    return 0

# # Add to profile view
# @csrf_exempt
# def profile_view(request, customer_id):
#     customer = get_object_or_404(User, id=customer_id)
#     average_rating = get_average_rating(customer_id)
#     ratings = CustomerRating.objects.filter(rated_customer=customer)

#     return render(request, 'profile.html', {
#         'customer': customer,
#         'average_rating': average_rating,
#         'ratings': ratings
#     })