from django.urls import path
from .views import Hello, ContactListView

urlpatterns = [
    path('hello/', Hello.as_view(), name='hello-world'),
    path('contacts/', ContactListView.as_view())
]