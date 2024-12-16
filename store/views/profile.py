from django.shortcuts import render, redirect, HttpResponseRedirect,get_object_or_404
# from store.models.category import Category
from store.models.connection import ConnectionRequest
from store.models.notifications import Notification
from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from store.models.customer import Customer, Skill
from store.models.customer_ratings import CustomerRating  # Import your Customer and Skill models
import json
from django.utils.timezone import now
from store.views.ratings import get_average_rating
from django.db.models import Count
from django.db.models import Q

class Profile1(View):
     # connection for particular user 
    # def get_connections_and_count(customer):
    #     # Fetch all connections where the customer is either the sender or receiver with status "accepted"
    #     connections = ConnectionRequest.objects.filter(
    #         Q(sender=customer, status="accepted") | Q(receiver=customer, status="accepted")
    #     )
    #     # Return the connections and their count
    #     return connections, connections.count()

    def get(self, request):
        customer_id = request.session.get('customer')  # Get the customer ID from session
        customer = Customer.objects.filter(id=customer_id).first()
        skills = list(customer.skills.values_list('name', flat=True)) if customer else []
        connections = ConnectionRequest.objects.filter(
            Q(sender=customer, status="accepted") | Q(receiver=customer, status="accepted")
        )
        # print(customer)
        connection_data = []
        for connection in connections:
            if connection.sender == customer:
                other_customer = connection.receiver
            else:
                other_customer = connection.sender
            
            # Add details about the connection
            connection_data.append({
                "id": other_customer.id,
                "first_name": other_customer.first_name,  # Assuming Customer has a `name` field
                "last_name": other_customer.last_name,
                "email": other_customer.email,  # Assuming Customer has an `email` field
                "image":other_customer.image.url
                # Add any additional fields you need for the template
            })
        if customer:
            # first_name = customer.first_name()  # Get all skills for this customer
            skills = customer.skills.all()
            data = {
                'customer': customer,
                'skills': skills,
                'connections':connection_data,
                'count':connections.count()
            }
        else:
            data = {}

        return render(request, 'profile.html', data)

    def post(self, request):
        try:
            data = json.loads(request.body)
            new_skills = data.get('skills', [])
            customer_id = request.session.get('customer')
            customer = Customer.objects.filter(id=customer_id).first()

            if customer:
                # Get a set of current skill names for the customer
                current_skill_names = set(customer.skills.values_list('name', flat=True))

                # Iterate through the new skills list, add only if not already present
                for skill_name in new_skills:
                    if skill_name not in current_skill_names:
                        skill, created = Skill.objects.get_or_create(name=skill_name)
                        customer.skills.add(skill)  # Add the new skill
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Customer not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


    def delete_skill(request, skill_id):
        if request.method == 'POST':
            customer_id = request.session.get('customer')
            customer = Customer.objects.filter(id=customer_id).first()

            if customer:
                try:
                    skill = Skill.objects.get(id=skill_id)
                    customer.skills.remove(skill)
                    return JsonResponse({'status': 'success', 'message': 'Skill deleted successfully.'})
                except Skill.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Skill not found.'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

    def user(request, customer_id):
        customer = Customer.objects.filter(id=customer_id).first()
        # connection = ConnectionRequest.objects.filter(sender=request.user, receiver=customer, status="accepted").exists()
        # return render(request, 'profile.html', {'customer': customer, 'is_connected': connection})
        skills = list(customer.skills.values_list('name', flat=True)) if customer else []
        if customer:
            # first_name = customer.first_name()  # Get all skills for this customer
            skills = customer.skills.all()
            data = {
                'customer': customer,
                'skills': skills,
            }
        else:
            data = {}

        return render(request, 'profile1.html', data)

 
    # def send_request(request, receiver_id):
    #     sender_id = request.session.get('customer')  # Get the customer ID from the session
    #     if sender_id is None:
    #         return redirect('login')  # Redirect to login if sender ID is not in session

    #     sender = get_object_or_404(Customer, id=sender_id)
    #     receiver = get_object_or_404(Customer, id=receiver_id)

    #     # Check if a connection request already exists between sender and receiver
    #     conn_request, created = ConnectionRequest.objects.get_or_create(sender=sender, receiver=receiver)

    #     # If the request is newly created or previously withdrawn, set status to "sent"
    #     if created or conn_request.status == "withdrawn":
    #         conn_request.status = "sent"
    #     else:
    #         # Toggle the request to "withdrawn" if it's already "sent"
    #         conn_request.status = "withdrawn"

    #     conn_request.save()
    #     return redirect('requests_page')  # Redirect to the requests page

    # def accept_request(request, request_id):
    #     conn_request = get_object_or_404(ConnectionRequest, id=request_id)
    #     if conn_request.receiver_id == request.session.get('customer'):
    #         conn_request.status = "accepted"
    #         conn_request.save()
    #     return redirect('requests_page')

    def requests_page(request):
        receiver_id = request.session.get('customer')
        if receiver_id is None:
            return redirect('login')

        receiver = get_object_or_404(Customer, id=receiver_id)
        received_requests = ConnectionRequest.objects.filter(receiver=receiver, status="sent")

    # def requests_page(request):
    #     customer_id = request.session.get('customer')
    #     incoming_requests = ConnectionRequest.objects.filter(receiver_id=customer_id, status="sent")
    #     return render(request, 'requests.html', {'incoming_requests': incoming_requests})  

    #     return render(request, 'connection_requests.html', {'received_requests': received_requests})

    # def withdraw_request(request, request_id):
    #     connection_request = get_object_or_404(ConnectionRequest, id=request_id)
    #     if connection_request.sender == request.user:
    #         connection_request.delete()
    #     return redirect('user_profile', user_id=connection_request.receiver.id)

    # def user_profile(request, user_id):
    #     customer = get_object_or_404(Customer, id=user_id)
    #     connection_request = ConnectionRequest.objects.filter(
    #         sender=request.user, receiver=customer
    #     ).first()

    #     is_request_sent = connection_request is not None

    #     context = {
    #         "customer": customer,
    #         "is_request_sent": is_request_sent,
    #         "connection_request": connection_request,
    #     }
    #     return render(request, "user_profile.html", context)

    # def withdraw_request(request, request_id):
    #     connection_request = get_object_or_404(ConnectionRequest, id=request_id)
    #     if connection_request.sender == request.user:
    #         connection_request.delete()
    #     return redirect('user_profile', user_id=connection_request.receiver.id)

   

    def user_profile(request, user_id):
        print(user_id)
        customer = get_object_or_404(Customer, id=user_id)
        skills = list(customer.skills.values_list('name', flat=True)) if customer else []
        if customer:
            skills = customer.skills.all()
        if request.session.get('customer'):
            viewer_id = request.session.get('customer')
            viewer = Customer.objects.get(id=viewer_id)
            
            # Check connection status
            connection_request = ConnectionRequest.objects.filter(
                sender=viewer, receiver=customer
            ).first()
            is_connected = connection_request and connection_request.status == "accepted"
            
            # Determine visibility
            show_full_profile = is_connected or viewer == customer

            average_rating = int(get_average_rating(user_id)) 
            ratings = CustomerRating.objects.filter(rated_customer=customer)
            stars_range = range(int(average_rating))
            
            star_counts = (
                CustomerRating.objects.filter(rated_customer=customer).values('stars')  # Group by 'rating'
                .annotate(count=Count('stars'))  # Count each group
                .order_by('-stars')  # Optional: Order by descending rating
            )

            star_counts_dict = {star: 0 for star in range(5, 0, -1)}
            for star_count in star_counts:
                star_counts_dict[star_count['stars']] = star_count['count']

            return render(request, "profile1.html", {
                "customer": customer,
                "is_connected": is_connected,
                "show_full_profile": show_full_profile,
                "connection_request": connection_request,
                'average_rating': average_rating,
                'ratings': ratings,
                'skills': skills,
                'stars_range': stars_range,
                'star_counts': star_counts_dict,
            })
        else:
            show_full_profile = customer

            
            average_rating = int(get_average_rating(user_id)) 
            ratings = CustomerRating.objects.filter(rated_customer=customer)
            stars_range = range(int(average_rating))
            
            star_counts = (
                CustomerRating.objects.filter(rated_customer=customer).values('stars')  # Group by 'rating'
                .annotate(count=Count('stars'))  # Count each group
                .order_by('-stars')  # Optional: Order by descending rating
            )

            star_counts_dict = {star: 0 for star in range(5, 0, -1)}
            for star_count in star_counts:
                star_counts_dict[star_count['stars']] = star_count['count']

            is_connected = "accepted"
            return render(request, "profile1.html", {
                "customer": customer,
                'ratings': ratings,
                'stars_range': stars_range,
                'star_counts': star_counts_dict,
                'average_rating': average_rating,
                'skills': skills,
                # "is_connected": is_connected,
                "show_full_profile": show_full_profile,
                # "connection_request": connection_request,
            })

    def send_request(request, receiver_id):
        if request.session.get('customer'):
            sender_id = request.session.get('customer')
            sender = get_object_or_404(Customer, id=sender_id)
            receiver = get_object_or_404(Customer, id=receiver_id)

            connection_request, created = ConnectionRequest.objects.get_or_create(sender=sender, receiver=receiver)
            if created or connection_request.status == "withdrawn":
                connection_request.status = "sent"
                connection_request.save()
            
            Notification.objects.create(
                sender=connection_request.sender,
                receiver=connection_request.receiver,
                message=f"{sender.first_name} connection request sent to the {receiver.first_name}."
            )
            return redirect('user_profile',receiver_id)
        else:
            returnUrl = request.META['PATH_INFO']
            return redirect(f'/login?return_url={returnUrl}')

    def withdraw_request(request, request_id):
        connection_request = get_object_or_404(ConnectionRequest, id=request_id)
        print(connection_request.receiver.id)
        if connection_request.sender.id == request.session.get('customer'):
            connection_request.status = "withdrawn"
            connection_request.save()
        return redirect('user_profile',connection_request.receiver.id)

    def accept_request(request, request_id):
        connection_request = get_object_or_404(ConnectionRequest, id=request_id)
        
        # Ensure the logged-in user is the intended receiver of the request
        if connection_request.receiver.id == request.session.get('customer'):
            # Update the connection request status to "accepted"
            connection_request.status = "accepted"
            connection_request.save()
            
            # Check if a connection already exists between the users (one direction check)
            if not ConnectionRequest.objects.filter(
                sender=connection_request.sender, receiver=connection_request.receiver
            ).exists():
                
                # Create a mutual connection
                ConnectionRequest.objects.create(sender=connection_request.sender, receiver=connection_request.receiver)

                # Create a notification for the sender
        Notification.objects.create(
            sender=connection_request.receiver,
            receiver=connection_request.sender,
            message=f"{connection_request.receiver.first_name} accepted your connection request."
        )
        customer = get_object_or_404(Customer, id=connection_request.receiver.id)
        message = 'You are now connected with the ' + customer.first_name +" "+customer.last_name  
        return render(request,'connection_requests.html',{"message":message})

    def reject_request(request, request_id):
        connection_request = get_object_or_404(ConnectionRequest, id=request_id)
        if connection_request.receiver.id == request.session.get('customer'):
            connection_request.status = "rejected"
            connection_request.save()
            Notification.objects.create(
                receiver=connection_request.sender,
                sender=connection_request.receiver,
                message=f"{connection_request.receiver.first_name} rejected your connection request."
            )
        return redirect('requests_page')
    
    def requests_page(request):
        customer_id = request.session.get('customer')
        customer = Customer.objects.get(id=customer_id)
        received_requests = ConnectionRequest.objects.filter(receiver=customer, status="sent")
        return render(request, 'connection_requests.html', {'received_requests': received_requests})

    def notifications_page(request):
        customer_id = request.session.get('customer')
        notifications = Notification.objects.filter(receiver_id=customer_id).order_by('-created_at')
        
        # Mark all notifications as read when viewing the page
        notifications.update(is_read=True)
        
        return render(request, 'notifications.html', {'notifications': notifications})

    def index(request):
        return render(request, "chat/index.html")

    def room(request, room_name):
        return render(request, "chat/room.html", {"room_name": room_name})

    