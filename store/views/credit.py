# views/credit.py

from django.shortcuts import render
from django.db.models import Q  # Import Q for complex queries
from store.models.customer import Customer
from store.models.connection import ConnectionRequest
from django.db.models import F
from django.http import JsonResponse
import json

 # Assuming Skill is in the same module

def send_credit(request):
    if request.method == 'POST':
        print('we are inside post')
        try:
            data = json.loads(request.body)  # Parse JSON from the request body
            email = data.get('email')  # Receiver's email
            credit_to_transfer = int(data.get('credit'))  # Credits to transfer
            print('we are inside try > after value fatching')
            
            sender_id = request.session.get('customer')  # Assuming logged-in user is the sender
            print(sender_id)
            senderCustomer = Customer.objects.filter(id=sender_id).first()

            if senderCustomer.email == email:
                return JsonResponse({"error": "You cannot send credits to your own email address.","success":False}, status=400)
            print('we are inside try > self -checking')
            # Check if receiver exists
            try:
                receiver = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return JsonResponse({"error": "The email address does not belong to any user."}, status=404)
            print('we are inside try > after receiver fatching')

            # Check if sender and receiver are connected
            connection = ConnectionRequest.objects.filter(
                sender=senderCustomer, receiver=receiver, status="accepted"
            ).exists() or ConnectionRequest.objects.filter(
                sender=receiver, receiver=senderCustomer, status="accepted"
            ).exists()


            if not connection:
                return JsonResponse({"error": "You are not connected with the receiver.","success":False}, status=403)

            print('we are inside try > after connection checking')
            # Check if sender has enough credits
            if senderCustomer.credit < credit_to_transfer:
                return JsonResponse({"error": "You do not have enough credits to complete this transaction.","success":False}, status=400)

            # Perform the transaction
            senderCustomer.credit = F('credit') - credit_to_transfer
            receiver.credit = F('credit') + credit_to_transfer
            senderCustomer.save(update_fields=['credit'])
            receiver.save(update_fields=['credit'])
            
            print('we are inside try > after saving values')
            return JsonResponse({"message": f"Successfully sent {credit_to_transfer} credits to {receiver.email}.",
            "success":True})
        
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}","success":False}, status=500)

    return JsonResponse({"error": "Invalid request method.","success":False}, status=405)