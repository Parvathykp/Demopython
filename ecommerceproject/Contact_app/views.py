from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django import forms
from .models import Contact
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            subject = "Welcome to Babysmile"
            message = "Our team will contact you within 24hrs."
            email_from = 'babysmileapp2024@gmail.com'
            email = form.cleaned_data['email']
            recipient_list = 'parvathykp92@gmail.com'
            send_mail(subject, message, email_from, [recipient_list])
            return render(request, 'success.html')
    form = ContactForm()
    context = {'form': form}
    return render(request, 'contact.html', context)



