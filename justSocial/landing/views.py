from django.shortcuts import render
from django.views import View
# Create your views here.


def Index(request):
   user=request.user
   context={'user':user}
   return render(request, 'index.html',context)
