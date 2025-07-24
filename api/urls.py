from django.urls import path
from .views import ContactListView, ContactDetailView

urlpatterns = [
    path('contacts/', ContactListView.as_view()),
    path('contacts/<int:id>/', ContactDetailView.as_view())
]