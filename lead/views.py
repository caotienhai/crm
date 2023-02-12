from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import Lead, Team
from client.models import Client

class LeadListView(LoginRequiredMixin,ListView):
    model = Lead
    
    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(created_by = self.request.user, converted_to_client = False)
    
class LeadDetailView(LoginRequiredMixin,DetailView): 
    model = Lead
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
    def get_object(self):
        queryset = super(LeadDetailView, self).get_queryset()        
        return queryset.filter(created_by=self.request.user,pk=self.kwargs.get('pk'))

class LeadUpdateView(LoginRequiredMixin,UpdateView):
    model = Lead    
    fields = ('contact_name','company_name','address','country','phone','email','profile','priority','status',)
    success_url = reverse_lazy('leads:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Lead'

        return context
    
    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

class LeadCreateView(LoginRequiredMixin,CreateView):
    model = Lead    
    fields = ('contact_name','company_name','address','country','phone','email','profile','priority','status',)
    success_url = reverse_lazy('leads:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by=self.request.user)[0]
        context['team'] = team
        context['title'] = 'Add lead'

        return context

    def form_valid(self, form):
        team = Team.objects.filter(created_by=self.request.user)[0]

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = team
        self.object.save()
        
        return redirect(self.get_success_url())
    
class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class ConvertView(View):
    def post(self, request, *args, **kwargs):
        pk=self.kwargs.get('pk')        
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = Team.objects.filter(created_by=request.user)[0]
        
        client = Client.objects.create(
            team = team,
            contact_name = lead.contact_name,
            company_name = lead.company_name,
            address = lead.address,
            country = lead.country,
            phone = lead.phone,
            email = lead.email,
            profile = lead.profile,
            created_by = request.user,
        ) 
        lead.converted_to_client = True
        lead.status = '5.ordered'
        lead.save()
        messages.success(request,'The Lead Has Been Converted!')
        return redirect('leads:list')