from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

import os
import csv
import googlemaps
#from .forms import CsvModelForm

# Create your views here.
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
    context = {}
    if "GET" == request.method:
        return render(request, "pinpoint.html", {'name': ''})
        # if not GET, then proceed

    csv_file = request.FILES["csv_file"]
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'File is not CSV type')
        return HttpResponseRedirect(reverse("upload_csv"))

    fs = FileSystemStorage()
    name = fs.save(csv_file.name, csv_file)
    context['name'] = name
    context['file_obj'] = csv_file

    return render(request, "pinpoint.html", context)

def process_csv(request, csv_file):

    gmaps = googlemaps.Client(key='AIzaSyDbEgQ2Imxzdp1dsbi1IXM1nYAgTuhuszY')

    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = output.csv'
    writer = csv.writer(response)

    for line in lines:
        address = line
        geocode_result = gmaps.geocode(address)[results][0]
        latitude =  geocode_result.get('geometry', {}).get('location', {}).get('lat', 0)
        longitude =  geocode_result.get('geometry', {}).get('location', {}).get('lng', 0)

        output_line = [address, latitude, longitude]
        writer.writerow(output_line)

    return response
