from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

import os
import json
import logging
import requests
import googlemaps
#from .forms import CsvModelForm

# Create your views here.
def testing(request):
    return render(request, 'pinpoint.html')

'''
def upload_csv(request):
    if request.method == 'POST':
        import pdb;pdb.set_trace()
        csv_file_name = request.FILES['csv_file']
        data = {
            'title': csv_file_name,
            'csv_file': request.FILES
        }
        form = CsvModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('upload_csv'))

    else:
        form = CsvModelForm()
        return render(request, 'pinpoint.html', {'form': form})
'''

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "pinpoint.html", data)
        # if not GET, then proceed

    csv_file = request.FILES["csv_file"]
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'File is not CSV type')
        return HttpResponseRedirect(reverse("upload_csv"))

    gmaps = googlemaps.Client(key='AIzaSyDbEgQ2Imxzdp1dsbi1IXM1nYAgTuhuszY')

    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")
    fname = os.path.splitext(os.path.basename(csv_file.name))[0]
    for line in lines:
        address = line
        geocode_result = gmaps.geocode(address)
        break

    return HttpResponse(geocode_result)
