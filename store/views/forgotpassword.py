from django.shortcuts import render, redirect
from store.models.customer import Customer
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import make_password

# Generate token for password reset
token_generator = PasswordResetTokenGenerator()

# Forgot Password View
def forgot_password(request):
    if request.session.get('customer'):
        return redirect('homepage')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            try:
                user = Customer.objects.filter(email=email).first()
                print(user)
                if user == None:
                    messages.error(request, 'No account found with this email.')
                else:
                # token = token_generator.make_token(user.id)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    reset_link = request.build_absolute_uri(f"/reset-password/{uid}/")
                    
                    # Send email (use proper email backend in production)
                    send_mail(
                        'Password Reset Request',
                        f"Click the link to reset your password: {reset_link}",
                        'devangp539@gmail.com',
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Password reset link has been sent to your email.')
            except Customer.DoesNotExist:
                messages.error(request, 'No account found with this email.')

            return redirect('forgot_password')

    
    return render(request, 'forgot_password.html')

# Reset Password View
def reset_password(request, uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
        print(user)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None

    if user is not None:
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password == confirm_password:
                user.password = make_password(password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        
        return render(request, 'reset_password.html', {'valid_link': True})
    else:
        messages.error(request, 'Invalid or expired link.')
        return redirect('forgot_password')
