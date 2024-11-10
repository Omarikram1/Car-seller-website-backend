from django.shortcuts import redirect, render
from rest_framework.views import APIView
from mainapp.forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from ..tokens import email_verification_token
from django.utils.encoding import force_str 
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from ..tokens import email_verification_token  # Ensure tokens.py exists and is correctly imported
from django.conf import settings


    



class SignupView(APIView):
  
  
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form, 'error': 'Form is invalid.'})
       

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)    
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False  
            user.save()
            user_id = user.pk
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('email_verification.html', {
                'uid': urlsafe_base64_encode(force_bytes(user_id)),  
                'token': email_verification_token.make_token(user),  
                'domain': current_site.domain,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            print("ERROR AAN LGA EE")
            return redirect('emailsent') 
        else:
            return render(request, 'signup.html', {'form': form, 'error': 'Form is invalid.'})




def LoginView(request):

    if (request.method == 'GET'):
        return render(request, 'login.html')
    
    if(request.method == 'POST'):
        pass
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
        



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        return render(request, 'email_invalid.html')

    if email_verification_token.check_token(user, token):   
        user.is_active = True
        user.save()

        messages.success(request, 'Your account has been activated successfully! You can now log in.')
        print("Hello world")
        return redirect('login')  
    else:
        return render(request, 'email_invalid.html')  


def sendemail(request):
    return render(request, 'email_sent.html')




def landingpage(request):
    return render(request, 'landingpage.html')





































