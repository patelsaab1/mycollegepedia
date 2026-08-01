from .models import Country, State, Religion, Category
from .serializers import CountrySerializer, StateSerializer, ReligionSerializer, CategorySerializer
from rest_framework import generics
from django.shortcuts import redirect

# Create your views here.
def welcome_redirect(request):
    return redirect('admin:index')


class ReligionList(generics.ListCreateAPIView):
    queryset = Religion.objects.all()
    serializer_class = ReligionSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class StateList(generics.ListAPIView):
    serializer_class = StateSerializer

    def get_queryset(self):
        country_id = self.request.query_params.get('country_id', None)
        if country_id is not None:
            queryset = State.objects.filter(country_id=country_id)
        else:
            queryset = State.objects.all()

        return queryset