from django.urls import path
from .views import indexPageView
from .views import profilePageView, storeProfilePageView
from .views import labVitalsPageView, storeVitalsPageView
from .views import FoodEntryPageView, FoodEntrySubmitPageView
from .views import FoodPageView, FoodSearchPageView, FoodSelectPageView, FoodTotalPageView
from .views import dashboardPageView, dashboardMealPageView, dashboardNutrientsPageView
from .views import JournalPageView, storeJournalPageView
from .views import ExercisePageView, storeExercisePageView
# new
from .views import loginPageView
from . import views


urlpatterns = [
    path('', indexPageView, name='index'),

    path('profile', profilePageView, name='profile'),
    path('storeprofile', storeProfilePageView, name='storeprofile'),

    path('labvitals', labVitalsPageView, name='labvitals'),
    path('storevitals', storeVitalsPageView, name='storevitals'),

    path("foodentry", FoodEntryPageView, name='FoodEntry'),
    path("foodSubmit", FoodEntrySubmitPageView, name='FoodEntrySubmit'),

    path("food", FoodPageView, name="food"),
    path("foodSearch/", FoodSearchPageView, name='FoodSearch'),
    path("foodSelect/", FoodSelectPageView, name='FoodSelect'),
    path("foodTotal/", FoodTotalPageView, name='FoodTotal'),

    path("dashboard", dashboardPageView, name='dashboard'), 
    path("dashboardSelect", dashboardPageView, name='dashboardSelect'),
    path("dashboardMeal", dashboardMealPageView, name='dashboardMeal'),
    path("dashboardMealSelect", dashboardMealPageView, name='dashboardMealSelect'),
    path("dashboardNutrients", dashboardNutrientsPageView, name='dashboardNutrients'),
    path("dashboardDateSelect", dashboardNutrientsPageView, name='dashboardDateSelect'),

    path("journal", JournalPageView, name='journal'), 
    path("storejournal", storeJournalPageView, name='storejournal'),

    path("exercise", ExercisePageView, name='exercise'), 
    path("storeexercise", storeExercisePageView, name='storeexercise'),

    # new
    path('login/', loginPageView, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
]