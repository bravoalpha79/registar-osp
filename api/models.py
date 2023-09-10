from django.contrib.gis.db import models


class SafetyObject(models.Model):
    naziv_objekta = models.CharField(max_length=255)
    ps_br = models.CharField(max_length=10, null=True, blank=True)
    e_br = models.CharField(max_length=10, null=True, blank=True)
    tip_objekta = models.IntegerField(null=True, blank=True)
    lucka_kapetanija = models.CharField(max_length=50, null=True, blank=True)
    fotografija = models.CharField(null=True, blank=True)
    id_ais = models.CharField(max_length=50, null=True, blank=True)
    simbol_oznaka = models.CharField(null=True, blank=True)

    lokacija = models.PointField()

    def __str__(self):
        return self.naziv_objekta
