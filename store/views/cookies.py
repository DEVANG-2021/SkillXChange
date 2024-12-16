import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from store.models.customer import Customer

def track_daily_visits(request):
    # Retrieve customer_id from session
    customer_id = request.session.get('customer')  # Get the customer ID from session
    print(customer_id)
    customer = Customer.objects.filter(id=customer_id).first()
    # Retrieve the visit history cookie (default to an empty JSON if not present)
    visit_history = request.COOKIES.get('visit_history', '{}')
    
    # Parse the JSON string into a Python dictionary
    visit_history = json.loads(visit_history)
    
    # Get today's date in YYYY-MM-DD format
    today = datetime.now().strftime('%Y-%m-%d')
    name = customer.first_name + " "+ customer.last_name
    # Increment the visit count for today
    visit_count_today = visit_history.get(today, 0) + 1
    visit_history[today] = visit_count_today
    
    # Create a response object
    response = render(request, 'index.html', {
        'name': name,
        'visit_history': visit_history,
        'visit_count_today': visit_count_today,
    })
    
    # Update the visit history cookie (store it as a JSON string)
    response.set_cookie('visit_history', json.dumps(visit_history), max_age=30*24*60*60)  # 30 days
    
    return response
