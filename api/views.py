import json
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View

from .forms import SafetyObjectForm
from .models import SafetyObject


class SafetyObjectsApiView(View):
    def get(self, request):
        queryset = SafetyObject.objects.all()
        data = json.loads(serialize("geojson", queryset, geometry_field="lokacija"))['features']
        return JsonResponse({'data': data})

    def post(self, request):
        post_data = json.loads(request.body)

        if not post_data.get('lokacija'):
            return JsonResponse({'data': {}, 'error': 'Location data must not be empty.'}, status=400)

        form = SafetyObjectForm(post_data)

        if form.is_valid():
            new_object = form.save(commit=False)
            loc_string = post_data['lokacija']
            try:
                loc_data = tuple([float(coord) for coord in loc_string.split(',')[:2]])
                loc = Point(loc_data)
            except (TypeError, ValueError):
                return JsonResponse({'data': {}, 'error': 'Submitted location data is invalid.'}, status=400)

            new_object.lokacija = loc
            new_object.save()
            return redirect('safety_object', object_id=new_object.id)
        else:
            return JsonResponse({'data': {}, 'error': form.errors}, status=400)


class SafetyObjectApiView(View):
    def get(self, request, object_id):
        try:
            obj = SafetyObject.objects.get(pk=object_id)
            queryset = [obj]
            data = json.loads(serialize("geojson", queryset, geometry_field="lokacija"))['features'][0]
            return JsonResponse({'data': data})
        except ObjectDoesNotExist:
            message = f'Object with id={object_id} not found.'
            return JsonResponse({'data': {}, 'error': message}, status=404)

    def patch(self, request, object_id):
        try:
            obj = SafetyObject.objects.get(pk=object_id)
        except ObjectDoesNotExist:
            message = f'Object with id={object_id} not found.'
            return JsonResponse({'data': {}, 'error': message}, status=404)

        patch_data = json.loads(request.body)
        form = SafetyObjectForm(patch_data, instance=obj)

        if form.is_valid():
            updated_object = form.save(commit=False)
            if 'lokacija' in patch_data:
                if not patch_data['lokacija']:
                    return JsonResponse({'data': {}, 'error': 'Location data must not be empty.'}, status=400)
                loc_string = patch_data['lokacija']
                try:
                    loc_data = tuple([float(coord) for coord in loc_string.split(',')[:2]])
                    loc = Point(loc_data)
                except (TypeError, ValueError):
                    return JsonResponse({'data': {}, 'error': 'Submitted location data is invalid.'}, status=400)

                updated_object.lokacija = loc

            updated_object.save()
            return redirect('safety_object', object_id=object_id)
        else:
            return JsonResponse({'data': {}, 'error': form.errors}, status=400)

    def delete(self, request, object_id):
        try:
            obj_to_delete = SafetyObject.objects.get(pk=object_id)
            obj_to_delete.delete()
            message = f'Object with id={object_id} successfully deleted.'
            return JsonResponse({'data': message})
        except ObjectDoesNotExist:
            message = f'Object with id={object_id} not found.'
            return JsonResponse({'data': {}, 'error': message}, status=404)
