from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('submit-contact/', views.submit_contact, name='submit_contact'),
    path('submit-faq/', views.submit_faq, name='submit_faq'),
]

