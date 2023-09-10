from django.contrib.gis.geos import Point
from django.db import connection
from django.test import TestCase, Client
from .models import SafetyObject


class ApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # reset ID autoincrement (to facilitate testing)
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval('api_safetyobject_id_seq', 1, FALSE)")

        self.object_1 = SafetyObject.objects.create(
            naziv_objekta="Test 1",
            ps_br="1111",
            e_br="11",
            tip_objekta=1,
            lucka_kapetanija="Zadar",
            fotografija=None,
            id_ais=None,
            simbol_oznaka="/path/oznaka1.png",
            lokacija=Point(11.4444, 11.5555)
        )

        self.object_2 = SafetyObject.objects.create(
            naziv_objekta="Test 2",
            ps_br="2222",
            e_br="22",
            tip_objekta=2,
            lucka_kapetanija="Šibenik",
            fotografija="/fotografije/foto.jpg",
            id_ais="LDR-777",
            simbol_oznaka="/path/oznaka2.png",
            lokacija=Point(22.55, 22.77)
        )

    def test_get_all_objects_endpoint(self):
        get_response = self.client.get('/api/safety_objects/')
        self.assertEquals(get_response.status_code, 200)
        self.assertEquals(len(get_response.json()['data']), 2)
        self.assertEquals(
            get_response.json()['data'][0],
            {
                "type": "Feature",
                "id": self.object_1.id,
                "properties": {
                    "naziv_objekta": "Test 1",
                    "ps_br": "1111",
                    "e_br": "11",
                    "tip_objekta": 1,
                    "lucka_kapetanija": "Zadar",
                    "fotografija": None,
                    "id_ais": None,
                    "simbol_oznaka": "/path/oznaka1.png",
                    "pk": str(self.object_1.id)
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        11.4444,
                        11.5555
                    ]
                }
            }
        )

        self.assertEquals(
            get_response.json()['data'][1],
            {
                "type": "Feature",
                "id": self.object_2.id,
                "properties": {
                    "naziv_objekta": "Test 2",
                    "ps_br": "2222",
                    "e_br": "22",
                    "tip_objekta": 2,
                    "lucka_kapetanija": "Šibenik",
                    "fotografija": "/fotografije/foto.jpg",
                    "id_ais": "LDR-777",
                    "simbol_oznaka": "/path/oznaka2.png",
                    "pk": str(self.object_2.id)
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        22.55,
                        22.77
                    ]
                }
            }
        )

    def test_get_single_object_endpoint(self):
        get_response = self.client.get(f'/api/safety_objects/{self.object_2.id}')
        self.assertEquals(get_response.status_code, 200)
        self.assertEquals(
            get_response.json()['data'],
            {
                "type": "Feature",
                "id": self.object_2.id,
                "properties": {
                    "naziv_objekta": "Test 2",
                    "ps_br": "2222",
                    "e_br": "22",
                    "tip_objekta": 2,
                    "lucka_kapetanija": "Šibenik",
                    "fotografija": "/fotografije/foto.jpg",
                    "id_ais": "LDR-777",
                    "simbol_oznaka": "/path/oznaka2.png",
                    "pk": str(self.object_2.id)
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        22.55,
                        22.77
                    ]
                }
            }
        )

    def test_get_single_non_existing_object(self):
        get_response = self.client.get('/api/safety_objects/789')
        self.assertEquals(get_response.status_code, 404)
        self.assertEquals(get_response.json()['data'], {})
        self.assertEquals(get_response.json()['error'], 'Object with id=789 not found.')

    def test_create_new_object(self):
        new_object_data = {
            "naziv_objekta": "Novi Test",
            "ps_br": "3333",
            "e_br": "33",
            "tip_objekta": 3,
            "lucka_kapetanija": "Pula",
            "fotografija": '/fotografije/nova_fotografija.jpg',
            "id_ais": "LD-11",
            "simbol_oznaka": "/path/oznaka5.png",
            "lokacija": "33.33, 33.444"
        }

        post_response = self.client.post('/api/safety_objects/', new_object_data, content_type='application/json')
        self.assertEquals(post_response.status_code, 302)
        self.assertRedirects(post_response, '/api/safety_objects/3')

        get_response_single = self.client.get('/api/safety_objects/3')
        self.assertEquals(
            get_response_single.json()['data'],
            {
                "type": "Feature",
                "id": 3,
                "properties": {
                    "naziv_objekta": "Novi Test",
                    "ps_br": "3333",
                    "e_br": "33",
                    "tip_objekta": 3,
                    "lucka_kapetanija": "Pula",
                    "fotografija": "/fotografije/nova_fotografija.jpg",
                    "id_ais": "LD-11",
                    "simbol_oznaka": "/path/oznaka5.png",
                    "pk": "3"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        33.33,
                        33.444
                    ]
                }
            }
        )

        get_response_all = self.client.get('/api/safety_objects/')
        self.assertEquals(len(get_response_all.json()['data']), 3)

    def test_create_new_object_with_nonessential_fields_empty(self):
        new_object_data = {
            "naziv_objekta": "Novi Test",
            "ps_br": None,
            "e_br": None,
            "tip_objekta": None,
            "lucka_kapetanija": None,
            "fotografija": None,
            "id_ais": None,
            "simbol_oznaka": None,
            "lokacija": "33.33, 33.444"
        }

        post_response = self.client.post('/api/safety_objects/', new_object_data, content_type='application/json')
        self.assertEquals(post_response.status_code, 302)
        self.assertRedirects(post_response, '/api/safety_objects/3')

        get_response_single = self.client.get('/api/safety_objects/3')
        self.assertEquals(
            get_response_single.json()['data'],
            {
                "type": "Feature",
                "id": 3,
                "properties": {
                    "naziv_objekta": "Novi Test",
                    "ps_br": None,
                    "e_br": None,
                    "tip_objekta": None,
                    "lucka_kapetanija": None,
                    "fotografija": None,
                    "id_ais": None,
                    "simbol_oznaka": None,
                    "pk": "3"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        33.33,
                        33.444
                    ]
                }
            }
        )

        get_response_all = self.client.get('/api/safety_objects/')
        self.assertEquals(len(get_response_all.json()['data']), 3)

    def test_create_new_object_with_naziv_objekta_empty_or_missing(self):
        new_object_data = {
            "naziv_objekta": None,
            "ps_br": None,
            "e_br": None,
            "tip_objekta": None,
            "lucka_kapetanija": None,
            "fotografija": None,
            "id_ais": None,
            "simbol_oznaka": None,
            "lokacija": "33.33, 33.444"
        }

        post_response = self.client.post('/api/safety_objects/', new_object_data, content_type='application/json')
        self.assertEquals(post_response.status_code, 400)
        self.assertEquals(
            post_response.json()['error'],
            {"naziv_objekta": ["This field is required."]}
        )

        get_response_all = self.client.get('/api/safety_objects/')
        self.assertEquals(len(get_response_all.json()['data']), 2)

    def test_create_new_object_with_lokacija_empty_or_missing(self):
        new_object_data = {
            "naziv_objekta": "Novi Test",
            "ps_br": None,
            "e_br": None,
            "tip_objekta": None,
            "lucka_kapetanija": None,
            "fotografija": None,
            "id_ais": None,
            "simbol_oznaka": None
        }

        post_response = self.client.post('/api/safety_objects/', new_object_data, content_type='application/json')
        self.assertEquals(post_response.status_code, 400)
        self.assertEquals(
            post_response.json()['error'],
            'Location data must not be empty.'
        )

        get_response_all = self.client.get('/api/safety_objects/')
        self.assertEquals(len(get_response_all.json()['data']), 2)

    def test_create_new_object_with_lokacija_invalid(self):
        new_object_data = {
            "naziv_objekta": "Novi Test",
            "ps_br": None,
            "e_br": None,
            "tip_objekta": None,
            "lucka_kapetanija": None,
            "fotografija": None,
            "id_ais": None,
            "simbol_oznaka": None,
            "lokacija": "abc, 123"
        }

        post_response = self.client.post('/api/safety_objects/', new_object_data, content_type='application/json')
        self.assertEquals(post_response.status_code, 400)
        self.assertEquals(
            post_response.json()['error'],
            'Submitted location data is invalid.'
        )

        get_response_all = self.client.get('/api/safety_objects/')
        self.assertEquals(len(get_response_all.json()['data']), 2)

    def test_delete_object(self):
        delete_response = self.client.delete(f'/api/safety_objects/{self.object_1.id}')
        self.assertEquals(delete_response.status_code, 200)
        self.assertEquals(
            delete_response.json()['data'],
            f'Object with id={self.object_1.id} successfully deleted.'
        )

        get_response_all = self.client.get('/api/safety_objects/')
        self.assertEquals(len(get_response_all.json()['data']), 1)

        get_response_single = self.client.get(f'/api/safety_objects/{self.object_1.id}')
        self.assertEquals(get_response_single.status_code, 404)

    def test_delete_nonexisting_object(self):
        delete_response = self.client.delete('/api/safety_objects/789')
        self.assertEquals(delete_response.status_code, 404)
        self.assertEquals(
            delete_response.json()['error'],
            'Object with id=789 not found.'
        )

        get_response_all = self.client.get('/api/safety_objects/')
        self.assertEquals(len(get_response_all.json()['data']), 2)
