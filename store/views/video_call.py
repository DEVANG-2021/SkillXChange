from django.shortcuts import render, redirect
from store.models.customer import Customer
from store.models.meetings import Meeting

# Create your views here.

def videocall(request):
    if request.session.get('customer'):
        roomID = request.GET.get('roomID')
        meeting_object = Meeting.objects.filter(meeting_code=roomID).first()
        senderObject = Customer.objects.filter(id=request.session.get('customer')).first()
        return render(request, 'videocall_main.html', {'name': senderObject.first_name + " " + senderObject.last_name,'meeting_title':meeting_object.title})
    else:
        returnUrl = request.META['PATH_INFO']
        return redirect(f'/login?return_url={returnUrl}')

def join_room(request):
    if request.session.get('customer'):
        if request.method == 'POST':
            roomID = request.POST['roomID']
            return redirect("/meeting?roomID=" + roomID)
        return render(request, 'joinroom.html')
    else:
        returnUrl = request.META['PATH_INFO']
        return redirect(f'/login?return_url={returnUrl}')