import datetime
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    user = request.user
    #enviar usuario al render
    return render(request, 'detector/base.html', {'user': user})

