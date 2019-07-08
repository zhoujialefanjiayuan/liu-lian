from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def fly(request):
    user = request.GET.get('user')
    return render(request,'index.html',{'user':user})


def putscore(request):
    score = request.GET.get('score')
    user = request.GET.get("user")
    print(score,user)
    return  JsonResponse({'code':1})