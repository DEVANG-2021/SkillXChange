from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer, Skill

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        position = postData.get('position')
        address = postData.get('address')
        linkedin = postData.get('linkedin')
        twitter = postData.get('twitter')
        instagram = postData.get('instagram')
        facebook = postData.get('facebook')
        license_number = postData.get('license_number')

        # Check if an image file is uploaded; if not, set a default image
        image = request.FILES.get('image') or 'E:\Tools,Tehnologies and Projects\Eshop\Eshop-main\store\static\logo\profile.jpg'  # Path to default image

        license_image = request.FILES.get('license_image') or 'E:\Tools,Tehnologies and Projects\Eshop\Eshop-main\store\static\logo\license.jpg'

        # Validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'position': position,
            'address': address,
            'linkedin': linkedin,
            'twitter': twitter,
            'instagram': instagram,
            'facebook': facebook,
            'image': image,
            'license_number': license_number,
            'license_image': license_image,
        }

        error_message = None

        # Create Customer instance
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password,
            position=position,
            address=address,
            linkedin=linkedin,
            twitter=twitter,
            instagram=instagram,
            facebook=facebook,
            image=image,
            # license_number=license_number,
            # license_image=license_image,
        )
        
        error_message = self.validateCustomer(customer)

        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('login')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if not customer.first_name:
            error_message = "Please Enter your First Name !!"
        elif len(customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len(customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        # elif not customer.license_number:
        #     error_message = 'Please Enter your License Number'
        # elif not customer.license_number.isdigit():
        #     error_message = 'License Number must contain only digits'
        # elif len(customer.license_number) < 6 or len(customer.license_number) > 16:
        #     error_message = 'License Number must be between 6 and 16 digits'
        # elif not customer.license_image:
        #     error_message = 'Please Upload your License Image'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        
        return error_message

def update_image(request):
    customer_id = request.session.get('customer')
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            customer.image = image
            customer.save()
            return redirect('profile')  # Redirect to profile or relevant page
        else:
            return render(request, 'profile.html', {'error': 'Please upload a valid image.'})
    return render(request, 'profile.html', {'customer': customer})


def update_personal_details(request):
    customer_id = request.session.get('customer')
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.first_name = request.POST.get('first_name', customer.first_name)
        customer.last_name = request.POST.get('last_name', customer.last_name)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.position = request.POST.get('position', customer.position)
        customer.address = request.POST.get('address', customer.address)
        customer.save()
        return redirect('profile')  # Redirect to profile or relevant page
    return render(request, 'profile.html', {'customer': customer})


def update_social_links(request):
    customer_id = request.session.get('customer')
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.facebook = request.POST.get('facebook', customer.facebook)
        customer.instagram = request.POST.get('instagram', customer.instagram)
        customer.twitter = request.POST.get('twitter', customer.twitter)
        customer.linkedin = request.POST.get('linkedin', customer.linkedin)
        customer.save()
        return redirect('profile')  # Redirect to profile or relevant page
    return render(request, 'profile.html', {'customer': customer})


def update_license_details(request):
    customer_id = request.session.get('customer')
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.license_number = request.POST.get('license_number', customer.license_number)
        license_image = request.FILES.get('license_image')
        if license_image:
            customer.license_image = license_image
        customer.save()
        return redirect('profile')  # Redirect to profile or relevant page
    return render(request, 'profile.html', {'customer': customer})

