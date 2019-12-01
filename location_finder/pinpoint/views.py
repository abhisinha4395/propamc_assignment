from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import os
import csv
import googlemaps

# Create your views here.

def upload_csv(request):

    context = {}
    if "GET" == request.method:
        return render(request, "pinpoint.html", {'name': ''})
        # if not GET, then proceed

    csv_file = request.FILES.get("csv_file")
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'File is not CSV type. Upload another file')
        return HttpResponseRedirect(reverse("upload_csv"))

    fs = FileSystemStorage()
    name = fs.save(csv_file.name, csv_file)
    context['name'] = name

    return render(request, "pinpoint.html", context)

def process_csv(request):
    csv_file = request.GET.get('csv_file')
    csv_file = os.path.join(settings.MEDIA_ROOT, csv_file)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = output.csv'
    writer = csv.writer(response)

    gmaps = googlemaps.Client(key='AIzaSyDbEgQ2Imxzdp1dsbi1IXM1nYAgTuhuszY')
    file_data = open(csv_file)
    for line in file_data:
        address = line
        #import pdb; pdb.set_trace()
        geocode_result = gmaps.geocode(address)[0]
        latitude =  geocode_result.get('geometry', {}).get('location', {}).get('lat', 0)
        longitude =  geocode_result.get('geometry', {}).get('location', {}).get('lng', 0)

        output_line = [address, latitude, longitude]
        writer.writerow(output_line)

    return response
