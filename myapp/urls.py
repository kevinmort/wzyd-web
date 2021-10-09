from django.urls import path
from .views import my_view
from .views import change_api_url_post


urlpatterns = [
    path('', my_view, name='my-view'),
    path('my_view', my_view),
    path('change_api_url_post', change_api_url_post)
]
