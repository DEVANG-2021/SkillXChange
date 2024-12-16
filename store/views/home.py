from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.product import Products
from store.models.category import Category
from django.views import View

from django.shortcuts import render, redirect, HttpResponseRedirect

from django.views import View
from django.http import JsonResponse
from store.models.customer import Customer, Skill  # Import your Customer and Skill models
import json
from datetime import datetime
# Create your views here.
class Index(View):

    def get(self, request):
        response = None  # Initialize response with a default value
        
        if request.session.get('customer'):
            customer_id = request.session.get('customer')  # Get the customer ID from session
            customer = Customer.objects.filter(id=customer_id).first()

            # Retrieve the visit history cookie (default to an empty JSON if not present)
            visit_history = request.COOKIES.get('visit_history', '{}')
            
            # Parse the JSON string into a Python dictionary
            visit_history = json.loads(visit_history)
            
            # Get today's date in YYYY-MM-DD format
            today = datetime.now().strftime('%Y-%m-%d')
            name = customer.first_name + " " + customer.last_name
            # Increment the visit count for today
            visit_count_today = visit_history.get(today, 0) + 1
            visit_history[today] = visit_count_today
            
            skills = list(customer.skills.values_list('name', flat=True)) if customer else []
            if customer:
                skills = customer.skills.all()
                response = render(request, 'index.html', {
                    'customer': customer,
                    'skills': skills,
                    'name': name,
                    'visit_history': visit_history,
                    'visit_count_today': visit_count_today,
                })
                # Update the visit history cookie (store it as a JSON string)
                response.set_cookie('visit_history', json.dumps(visit_history), max_age=30*24*60*60)  # 30 days
                return response
            else:
                response = {}

        if response:
            return render(request, 'index.html', response)
        else:
            return render(request, 'index.html')