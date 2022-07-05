from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.RegisterView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('home/',views.HomeView.as_view()),
    path('workshopHome/',views.WorkshopHomeView.as_view()),
    path('search/',views.SearchView.as_view()),
    path('nearby/',views.NearbyWorkshops.as_view()),
    path('bookService/',views.BookServices.as_view()),
    path('fetchWorks/',views.WorkshopWorks.as_view())
]