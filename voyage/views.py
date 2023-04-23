from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View, CreateView,FormView,DetailView,ListView #We can use FormModel instead of CreateView

from .models import *
from django.contrib.auth.models import User
from authentication.models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout

from django.db.models import Q 

from django.core.paginator import Paginator
from .froms import *

from django.core.mail import send_mail  

from django.conf import settings 

"""Home view"""
class HomeView(TemplateView):
    template_name="base.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        all_travel_list = Favorites.objects.all().order_by('-id')
        paginator = Paginator( all_travel_list,8)
        
        page_number = self.request.GET.get('page')

        travel_list = paginator.get_page(page_number)
        
        context['travels']= travel_list
        if len(all_travel_list) == 0:
            context['travels']= "Pas de travel pour le moment ...."
        return  context

"""Template views for Travel Inspiration"""
class TravelInspirationView(TemplateView):
    template_name="travel_inspiration.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)           
        
        all_travel_inspiration = TravelInspiration.objects.all().order_by('id')
        paginator = Paginator( all_travel_inspiration ,3)
        
        page_number = self.request.GET.get('page')

        travel_inspiration_list = paginator.get_page(page_number)
        
        context['travel_inspiartions']= travel_inspiration_list
        
        return  context

"""LIst views for Travel Inspiration"""
class TravelInspirationListView(ListView):
    template_name = "travel_inspiration_list.html"
    queryset = TravelInspiration.objects.all().order_by('-id')
    context_object_name = "travel_inspiration"

"""Create views for travel inspiration"""
class TravelInspirationCreateView(CreateView):
    template_name = "create_travel_inspiration.html"
    form_class = TravelInspirationForm
    successj_url = reverse_lazy('voyage:home')


""" Favorite list views"""
class FavoritesListView(ListView):
    template_name = "favorite.html"
    queryset = Favorites.objects.all().order_by('-id')
    context_object_name = "favorites"


class TravelInspirationDetailView(DetailView):
    template_name="travel-detail.html"
    model = TravelInspiration
    context_object_name = 'traval_inspirations'


""" Favorites details views"""
class FavoriteDetailView(DetailView):
    template_name="favorite-detail.html"
    model = Favorites
    context_object_name = 'favorite'


class CreateFavoriteView(View):
    def post(self,request, *args,**kwargs):
        if request.user.is_authenticated and CustomUser.objects.filter(user=request.user).exists():
            travel_id = self.kwargs["pk"]
            
            travel = TravelInspiration.objects.get (id=travel_id)
            user = request.user
            new_favorites =  Favorites.objects.create(travel_inspiration=travel)
            new_favorites.users.add(user)
            return redirect(reverse_lazy("voyage:favorite",kwargs = {"pk": travel_id}))


class TravelInspirationReSearchView(TemplateView):
    template_name = 'travel-research.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)  
        keyword = self.request.GET.get('travel_keyword')  
        context["keyword"] = keyword 
        print(f'{keyword},-----------------------------------------')
        """
        Nous recherchons tous les travel dont :
        - id est le mot clé ou 
        - dont les activites, date de debut et date de fin  continnes le mot clé
         
        """
        context["found_travels"] = TravelInspiration.objects.filter(Q(id=int(keyword)) | Q(prefered_activitties__contains=keyword)\
            | Q(travel_date_start__contains=keyword) | Q(travel_date_end__contains=keyword))
        return context  
    


"""
TODO : 
- terminer correctement la logique des vues 
- aller implementer le template
- voir les urls 
- tester  le le template 
- faire appel à l'API dans la vue



REprezndre le ssysteme d'authentification en créant autre APP 
et ne plus tenir compte de JWT pour l'instant

"""