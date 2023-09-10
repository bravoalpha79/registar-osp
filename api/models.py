from django.contrib.gis.db import models


class SafetyObject(models.Model):
    naziv_objekta = models.CharField(max_length=255)
    ps_br = models.CharField(max_length=10, null=True)
    e_br = models.CharField(max_length=10, null=True)
    tip_objekta = models.IntegerField(null=True)
    lucka_kapetanija = models.CharField(max_length=50, null=True)
    fotografija = models.URLField(null=True)
    id_ais = models.CharField(max_length=50, null=True)
    simbol_oznaka = models.URLField(null=True)

    lokacija = models.PointField()

    def __str__(self):
        return self.naziv_objekta
