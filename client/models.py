from django.db import models
from django.contrib.auth.models import User
from team.models import Team

class Client(models.Model):
    team = models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=70)
    address = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=30)
    phone = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    profile = models.TextField(blank=True,null=True)    
    created_by = models.ForeignKey(User, related_name='clients',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('contact_name',)
    
    def __str__(self) -> str:
        return self.contact_name