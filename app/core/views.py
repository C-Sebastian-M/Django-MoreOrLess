from django.shortcuts import render

def inicio(request):
    return render(request, 'index.html')
def presupuesto(request):
    return render(request, 'presupuesto.html')
# Create your views here.
