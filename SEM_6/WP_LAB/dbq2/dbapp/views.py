from django.shortcuts import render,redirect
from .models import Works, Lives
from .forms import WorksForm, LivesForm

# Create your views here.

def index(request):
    works = Works.objects.all()
    return render(request,'index.html',{'works':works})

def add_works(request):
    if request.method =='POST':
        form = WorksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = WorksForm()
    return render(request,'add_works.html',{'form':form})

def find(request):
    if request.method =='POST':
        company = request.POST.get('company')
        ob = Works.objects.filter(company=company)

        ret =[]
        for work in ob:
            person = Lives.objects.filter(name=work)
            for p in person:
                ret.append({'name':work.name,'city':p.city})
        return render(request,'find.html',{'ret':ret})
    else:
        return render(request,'find.html')


