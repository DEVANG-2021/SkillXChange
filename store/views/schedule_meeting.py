from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from store.models.customer import Customer
from store.models.connection import ConnectionRequest
from store.models.meetings import Meeting
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.db.models import Q
from datetime import datetime

def schedule_meeting_page(request):
    main_customer_id = request.session.get('customer')
    senderObject = Customer.objects.filter(id=main_customer_id).first()
    connected_customers = ConnectionRequest.objects.filter(
        (Q(sender=senderObject) | Q(receiver=senderObject)) & 
        Q(status="accepted")
    ).exclude(id=main_customer_id)
    customers = [
        conn.receiver if conn.sender == senderObject else conn.sender
        for conn in connected_customers
    ]
    return render(request, 'schedule_meeting.html', {'connected_customers': customers})

@csrf_exempt
def schedule_meeting(request):
    if request.method == 'POST':
        print('we are here')
        data = json.loads(request.body)
        meeting_title = data.get('meeting_title')
        meeting_date = data.get('meeting_date')  # Expected format: 'YYYY-MM-DD'
        meeting_time = data.get('meeting_time')  # Expected format: 'HH:MM'
        selected_customers = data.get('selected_customers')  # List of selected customer emails
        sender_id = request.session.get('customer')
        sender = Customer.objects.filter(id=sender_id).first() # Assuming the logged-in user is the sender
        
        print('we are here----')
        if not meeting_title or not selected_customers or not meeting_date or not meeting_time:
            return JsonResponse({"error": "Meeting title, date, time, and customers are required."}, status=400)

        # Validate meeting_date and meeting_time
        try:
            scheduled_datetime = datetime.strptime(f"{meeting_date} {meeting_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return JsonResponse({"error": "Invalid date or time format."}, status=400)

        # Generate unique link and meeting code
        
        # meeting_code = get_random_string(8).upper()
        meeting_code = random.randint(1000, 9999)
        
        meeting_link = f"http://127.0.0.1:8000/meeting?roomID={meeting_code}"  # Update with your domain
        print('after meeting')
        # Check connections and send emails
        valid_customers = []
        for email in selected_customers:
            try:
                receiver = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                continue  # Skip if customer does not exist

            # Check if the sender and receiver are connected
            connection = ConnectionRequest.objects.filter(
                sender=sender, receiver=receiver, status="accepted"
            ).exists() or ConnectionRequest.objects.filter(
                sender=receiver, receiver=sender, status="accepted"
            ).exists()

            if connection:
                valid_customers.append(receiver)

        if not valid_customers:
            return JsonResponse({"error": "No valid connected customers found."}, status=400)

        print('after valid customer')        
        # Save meeting details in the Meeting object
        meeting = Meeting.objects.create(
            title=meeting_title,
            scheduled_by=sender,
            meeting_link=meeting_link,
            meeting_code=meeting_code,
            date=scheduled_datetime.date(),
            time=scheduled_datetime.time(),
            participant_emails=[customer.email for customer in valid_customers],
        )
        meeting.participants.set(valid_customers)
        print('after meeting object') 
        # Send email invitations
        for customer in valid_customers:
            send_mail(
                subject=f"You are invited to a meeting: {meeting_title}",
                message=(
                    f"{sender.first_name} {sender.last_name} has invited you to join a meeting.\n\n"
                    f"Meeting Title: {meeting_title}\n"
                    f"Meeting Date: {meeting_date}\n"
                    f"Meeting Time: {meeting_time}\n"
                    f"Meeting Link: {meeting_link}\n"
                    f"Meeting Code: {meeting_code}\n\n"
                    f"Please join the meeting using the link and meeting code provided."
                ),
                from_email="devangp539@gmail.com",  # Update with your email
                recipient_list=[customer.email],
            )
        print('after customer mail')  
        return JsonResponse({
            "message": f"Meeting scheduled successfully. Invitation sent to {len(valid_customers)} connections.",
            "meeting_link": meeting_link,
            "meeting_code": meeting_code,
        })
        print('after customer json object') 

    return JsonResponse({"error": "Invalid request method."}, status=405)



def scheduled_meetings(request):
    if request.session.get('customer'):
        main_customer_id = request.session.get('customer')
        senderObject = Customer.objects.filter(id=main_customer_id).first()
        meetings = Meeting.objects.filter(scheduled_by=main_customer_id)
        return render(request, 'scheduled_meetings.html', {'meetings': meetings})
    else:
        returnUrl = request.META['PATH_INFO']
        return redirect(f'/login?return_url={returnUrl}')