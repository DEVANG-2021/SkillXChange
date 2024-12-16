# from django.shortcuts import render, redirect, HttpResponseRedirect,get_object_or_404
# from django.http import JsonResponse
# import random
# import time
# from agora_token_builder import RtcTokenBuilder
# from store.models.roommembers import RoomMember
# from store.models.customer import Customer
# from store.models.meetings import Meeting
# import json
# from django.views.decorators.csrf import csrf_exempt

# # Create your views here.
# def lobby(request):
#     if request.session.get('customer'):
#         channelName = request.GET.get('channel')
#         return render(request, 'base/lobby.html',{'channelName': channelName})
#     else:
#         returnUrl = request.META['PATH_INFO']
#         return redirect(f'/login?return_url={returnUrl}')
    
# def room(request):
#     if request.session.get('customer'):
#         return render(request, 'base/room.html')
#     else:
#         returnUrl = request.META['PATH_INFO']
#         return redirect(f'/login?return_url={returnUrl}')
    
# def getToken(request):
#     if request.session.get('customer'):
#         main_customer_id = request.session.get('customer')
#         customerObject = Customer.objects.filter(id=main_customer_id).first()
#         # name = customerObject.first_name +" "+customerObject.last_name
#         data = json.loads(request.body)
#         channelName = request.GET.get('channel')
#         meeting_code = data.get('meeting_code')
#         meeting_object = Meeting.objects.filter(title=channelName,meeting_code=meeting_code).first()
#         # if meeting_object:
#         print('inside')
#         appId = "2cf378dede714a18820525e768b6ca48"
#         appCertificate = "300f66cec6934b1c9ca2dbcdebfc3133"
#         uid = random.randint(1, 230)
#         expirationTimeInSeconds = 3600
#         currentTimeStamp = int(time.time())
#         privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
#         role = 1
#         token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
#         return JsonResponse({'token': token, 'uid': uid}, safe=False)
#         # else:
#         #     message = 'Access Denied'
#         #     return JsonResponse({'message':message})
#     else:
#         returnUrl = request.META['PATH_INFO']
#         return redirect(f'/login?return_url={returnUrl}')


# @csrf_exempt
# def createMember(request):
#     data = json.loads(request.body)
#     member, created = RoomMember.objects.get_or_create(
#         name=data['name'],
#         uid=data['UID'],
#         room_name=data['room_name']
#     )

#     return JsonResponse({'name':data['name']}, safe=False)


# def getMember(request):
#     uid = request.GET.get('UID')
#     room_name = request.GET.get('room_name')

#     member = RoomMember.objects.get(
#         uid=uid,
#         room_name=room_name,
#     )
#     name = member.name
#     return JsonResponse({'name':member.name}, safe=False)

# @csrf_exempt
# def deleteMember(request):
#     data = json.loads(request.body)
#     member = RoomMember.objects.get(
#         name=data['name'],
#         uid=data['UID'],
#         room_name=data['room_name']
#     )
#     member.delete()
#     return JsonResponse('Member deleted', safe=False)


# New COde

from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from store.models.meetings import Meeting
from store.models.roommembers import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')


def getToken(request):
    appId = "2cf378dede714a18820525e768b6ca48"
    appCertificate = "300f66cec6934b1c9ca2dbcdebfc3133"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)