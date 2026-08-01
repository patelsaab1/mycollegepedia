from django.urls import path
from .views import CountryList,StateList,ReligionList,CategoryList

urlpatterns = [
    path('religion/', ReligionList.as_view(), name='religion'),
    path('category/', CategoryList.as_view(), name='category'),
    path('country/', CountryList.as_view(), name='country'),
    path('state/', StateList.as_view(), name='state'),
]
