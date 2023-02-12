from django.db import models
from django.contrib.auth.models import User
from team.models import Team

class Lead(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CHOICE_PRIORITY = ((LOW, 'low'),(MEDIUM, 'medium'),(HIGH, 'high'),)    
    
    FOLLOW = '1.follow-up'
    DEMANDED = '2.demanded'
    OFFERED = '3.offered'
    DEALING = '4.dealing'
    ORDERED = '5.ordered'
    LOST = '6.lost'
    
    CHOICE_STATUS = ((FOLLOW, '1.follow-up'),                                          
                     (DEMANDED, '2.demanded'),
                     (OFFERED, '3.offered'),
                     (DEALING, '4.dealing'),
                     (ORDERED, '5.ordered'),
                     (LOST, '6.lost'),)
    team = models.ForeignKey(Team, related_name='leads', on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=70)
    address = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=30,blank=True,null=True)
    phone = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    profile = models.TextField(blank=True,null=True)
    priority = models.CharField(max_length=10,choices=CHOICE_PRIORITY,default=MEDIUM)
    status = models.CharField(max_length=14,choices=CHOICE_STATUS,default=DEMANDED)
    converted_to_client = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='leads',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('contact_name',)
    
    def __str__(self) -> str:
        return self.contact_name