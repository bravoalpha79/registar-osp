import json
from django.contrib.gis.geos import Point
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import SafetyObject


class SafetyObjectsApiView(View):
    def get(self, request):
        queryset = SafetyObject.objects.all()
        data = json.loads(serialize("geojson", queryset, geometry_field="lokacija"))['features']
        return JsonResponse(data, safe=False)


class SafetyObjectApiView(View):
    def get(self, request, object_id):
        queryset = [SafetyObject.objects.get(pk=object_id)]
        data = json.loads(serialize("geojson", queryset, geometry_field="lokacija"))['features'][0]
        return JsonResponse(data)