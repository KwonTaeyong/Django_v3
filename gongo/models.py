from django.db import models
from common.models import User


class List(models.Model):
    sourceOrg = models.CharField(max_length=100, )
    sourceId = models.CharField(max_length=100)
    sourceUrl = models.URLField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=255)
    contents = models.TextField()
    pStDt = models.DateField(null=True, blank=True)
    pEdDt = models.DateField(null=True, blank=True)
    hostOrg = models.CharField(max_length=100, null=True, blank=True)
    hostName = models.CharField(max_length=100, null=True, blank=True)
    hostPhone = models.CharField(max_length=20, null=True, blank=True)
    hostEmail = models.EmailField(null=True, blank=True)
    views = models.IntegerField(default=0)
    scrapDt = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sourceOrg', 'sourceId'], name='unique_sourceOrg_sourceId')
        ]


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userId')
    gongo = models.ForeignKey(List, on_delete=models.CASCADE, related_name='gongoId')
    addDt = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'gongo'], name='unique_userId_gongoId')
        ]
