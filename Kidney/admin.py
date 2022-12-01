from django.contrib import admin

# Register your models here.

from .models import Person, Morbidity, LabVitals, Food, FoodEntry, JournalEntry, ExerciseEntry

admin.site.register(Person)
admin.site.register(Morbidity)
admin.site.register(LabVitals) 
admin.site.register(Food) 
admin.site.register(FoodEntry) 
admin.site.register(JournalEntry) 
admin.site.register(ExerciseEntry) 