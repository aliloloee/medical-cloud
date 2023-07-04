from django.shortcuts import render


def live(request) :
    return render(request, 'client/live.html')