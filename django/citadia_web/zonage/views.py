from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("""
    <h1>BIENVENUE sur CITADIA PLU Collaboratif</h1>
    <p>Cette plateforme sera le lieu d'échange entre les techniciens des collectivités et les collaborateurs du Groupe Citadia.</p>
    """)
