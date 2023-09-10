import json
from django.db import IntegrityError
from django.contrib.gis.geos import GEOSGeometry
from api.models import SafetyObject

with open('data.geojson') as f:
    data = json.load(f)
for ft in data['features']:
    properties = ft['properties']
    geom_str = json.dumps(ft['geometry'])
    geom = GEOSGeometry(geom_str)
    safety_object = SafetyObject(
        naziv_objekta = properties['naziv_objekta'],
        ps_br = properties['ps_br'],
        e_br = properties['e_br'],
        tip_objekta = properties['tip_objekta'],
        lucka_kapetanija = properties['lucka_kapetanija'],
        fotografija = properties['fotografija'],
        id_ais = properties['id_ais'],
        simbol_oznaka = properties['simbol_oznaka'],
        pk = int(properties['pk']),
        lokacija = geom
    )
    try:
        safety_object.save()
    except IntegrityError:
        safety_object.pk = None
        safety_object.save()
