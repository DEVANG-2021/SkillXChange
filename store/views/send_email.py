from django.core.mail import send_mail
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
def send_invitation_email(request):
    # subject = "Meeting Invitation"
    # message = "You are invited to join a meeting. <b>Please use the provided link and code.</b>"
    # recipient_list = ['parmardevang459@gmail.com']  # Replace with the recipient's email
    # from_email = None  # Optional; uses DEFAULT_FROM_EMAIL if None

    # try:
    #     send_mail(
    #         subject,
    #         message,
    #         from_email,
    #         recipient_list,
    #         fail_silently=False,
    #     )
    #     
    # except Exception as e:
    #     return JsonResponse({'error': str(e)})
    

    subject = "hello"
    from_email = "parmardevang459@gmail.com"
    to = "devangp539@gmail.com"
    text_content = "This is an important message."
    html_content = "<p>This is an <strong>important</strong> message.</p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return JsonResponse({'message': 'Email sent successfully!'})