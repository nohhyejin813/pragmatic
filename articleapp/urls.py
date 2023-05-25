from django.urls import path
from django.views.generic import TemplateView

from profileapp.views import ProfileCreateView, ProfileUpdateView


urlpatterns = [
    path('list/', TemplateView.as_view(template_name='articleapp/list.html'), name='list'),
]

