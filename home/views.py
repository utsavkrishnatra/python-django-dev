from django.shortcuts import render,HttpResponse
from datetime import datetime
from home.models import Contact
# Create your views here.
def index(request):
    return render(request,'index.html')


def contact(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
       
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        
        def __str__(self):
            self.name
            
        contact=Contact(name=name,email=email,phone=phone, date=datetime.today(),subject=subject,message=message)
        contact.save()
        
        
        
    return render(request,'contact.html')