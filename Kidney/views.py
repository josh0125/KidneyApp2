from django.shortcuts import render, redirect
import urllib.parse
import requests
from .models import Person, Morbidity
from .models import LabVitals
from .models import FoodEntry, Food
from .models import JournalEntry
from .models import ExerciseEntry

# NEW LOGIN IMPORTS
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def indexPageView(request):
    return render(request, 'kidney/index.html')

# Profile Views

def profilePageView(request):
    return render(request, 'kidney/profilepopup.html')

def storeProfilePageView(request):
    if request.method == 'POST':
        new_person = Person()

        new_person.first_name = request.POST.get('fName')
        new_person.last_name = request.POST.get('lName')
        new_person.phone = request.POST.get('phone')
        new_person.email = request.POST.get('email')
        new_person.address = request.POST.get('address')
        new_person.city = request.POST.get('city')
        new_person.state = request.POST.get('state')
        new_person.zip = request.POST.get('zipcode')
        new_person.age = request.POST.get(('age'))
        new_person.weight = request.POST.get(('weight'))
        new_person.height = request.POST.get(('height'))

        new_person.save()
        if (request.POST.get('HBP')):
            new_Morbidity = Morbidity.objects.create(name='High Blood Pressure', datediagnosed=request.POST.get('bloodDate'))
            new_person.morbidities.add(new_Morbidity)

        if (request.POST.get('DIA')):
            new_Morbidity = Morbidity.objects.create(name='Diabetes', datediagnosed=request.POST.get('diabetesDate'))
            new_person.morbidities.add(new_Morbidity)

    return render(request, 'kidney/profilepopup.html')

# Lab Vitals Views

def labVitalsPageView(request):
    return render(request, 'kidney/labvitals.html')

def storeVitalsPageView(request):
    if request.method == 'POST':
        person = Person.objects.get(personid=1)

        new_vitals = LabVitals()

        new_vitals.personid = person
        new_vitals.K = request.POST.get('k')
        new_vitals.Phos = request.POST.get('phos')
        new_vitals.Na = request.POST.get('na')
        new_vitals.Creatinine = request.POST.get('creatinine')
        new_vitals.Albumin = request.POST.get('albumin')
        new_vitals.BloodPressure = request.POST.get('blood')
        new_vitals.BloodSugar = request.POST.get('sugar')
        new_vitals.Date = request.POST.get('date')
        new_vitals.Weight = request.POST.get(('weight'))

        new_vitals.save()

    return render(request, 'kidney/index.html')

# Journal Entry Views

def JournalPageView(request):
    return render(request, 'kidney/journal.html')

def storeJournalPageView(request):
    if request.method == 'POST':
        person = Person.objects.get(personid=1)

        new_journal = JournalEntry()

        new_journal.personid = person
        new_journal.date = request.POST.get('date') 
        new_journal.notes = request.POST.get('notes') 
        new_journal.status = request.POST.get('status') 

        new_journal.save()

    return render(request, 'kidney/journal.html')

# Exercise Entry Views

def ExercisePageView(request):
    return render(request, 'kidney/exercise.html')

def storeExercisePageView(request):
    if request.method == 'POST':
        person = Person.objects.get(personid=1)

        new_exercise = ExerciseEntry()

        new_exercise.personid = person
        new_exercise.date = request.POST.get('date') 
        new_exercise.duration = request.POST.get('duration') 
        new_exercise.weight = request.POST.get('weight') 

        new_exercise.save()

    return render(request, 'kidney/exercise.html')

# Food Entry Views

def FoodEntryPageView(request) :
    return render(request, 'kidney/foodEntry.html')

def FoodEntrySubmitPageView(request):

    person = Person.objects.get(personid=1)

    new_foodEntry = FoodEntry()
    new_foodEntry.personid = person
    new_foodEntry.date = request.POST.get('date')
    new_foodEntry.mealType = request.POST.get('meal')

    new_foodEntry.save()

    return render(request, 'kidney/FoodSearch.html')


# Food Views

def FoodPageView(request) :
    return render(request, 'kidney/FoodSearch.html')


def FoodSearchPageView(request) :
    # Variables from the Search
    sName = request.GET['name']
    #iAmount = request.GET['amount']

    # Getting the ID of the specific food
    main_api = 'https://api.nal.usda.gov/fdc/v1/foods/search?api_key=hzFpuwTYK1oM4XS0SnGp0xJyNVQG7EI4Yq0ZK5dl&dataType=Survey%20%28FNDDS%29&'

    food = sName

    url = main_api + urllib.parse.urlencode({'query': food})

    new = requests.get(url).json()

    newID = new['foods'][0]['fdcId']

    data = {'name': sName.upper(), 'list': []}

    for iCount in range(0,1):
        newID = new['foods'][iCount]['fdcId']
        
        api2 = 'https://api.nal.usda.gov/fdc/v1/food/' + str(newID) + '?api_key=hzFpuwTYK1oM4XS0SnGp0xJyNVQG7EI4Yq0ZK5dl'

        new2 = requests.get(api2).json()

        print(newID)

        #print({'name': new2['foodNutrients'][1]['nutrient']['name'], 'amount': str(new2['foodNutrients'][1]['amount']), 'unitName' : str(new2['foodNutrients'][1]['nutrient']['unitName'])})

        data['list'].append({'description': new['foods'][iCount]['description'], 'additional': new['foods'][iCount]['additionalDescriptions'], 'number': new['foods'][iCount]['fdcId'], \
            'nutrients' : [{'name': new2['foodNutrients'][1]['nutrient']['name'], 'amount': str(new2['foodNutrients'][1]['amount']), 'unitName' : str(new2['foodNutrients'][1]['nutrient']['unitName'])}, \
                {'name': new2['foodNutrients'][3]['nutrient']['name'], 'amount': str(new2['foodNutrients'][3]['amount']), 'unitName' : str(new2['foodNutrients'][3]['nutrient']['unitName'])}, \
                    {'name': new2['foodNutrients'][8]['nutrient']['name'], 'amount': str(new2['foodNutrients'][8]['amount']), 'unitName' : str(new2['foodNutrients'][8]['nutrient']['unitName'])}, \
                        {'name': new2['foodNutrients'][13]['nutrient']['name'], 'amount': str(new2['foodNutrients'][13]['amount']), 'unitName' : str(new2['foodNutrients'][13]['nutrient']['unitName'])}, \
                            {'name': new2['foodNutrients'][14]['nutrient']['name'], 'amount': str(new2['foodNutrients'][14]['amount']), 'unitName' : str(new2['foodNutrients'][14]['nutrient']['unitName'])}, \
                                {'name': new2['foodNutrients'][15]['nutrient']['name'], 'amount': str(new2['foodNutrients'][15]['amount']), 'unitName' : str(new2['foodNutrients'][15]['nutrient']['unitName'])}, \
                                    {'name': new2['foodNutrients'][66]['nutrient']['name'], 'amount': str(new2['foodNutrients'][66]['amount']), 'unitName' : str(new2['foodNutrients'][66]['nutrient']['unitName'])}]})

    
    # Sending collected data to html
    context = {
        'food' : data
    }

    # Returning a Specific HTML
    return render(request, 'kidney/foodSelect.html', context)

def FoodSelectPageView(request) :
    # Variables from the Search
    sName = request.GET['name']
    newID = request.GET['number']

    # Get Nutrients from ID
    api2 = 'https://api.nal.usda.gov/fdc/v1/food/' + str(newID) + '?api_key=hzFpuwTYK1oM4XS0SnGp0xJyNVQG7EI4Yq0ZK5dl'

    new2 = requests.get(api2).json()

    data = {'name': sName, 'number': newID, 'amount': 1, 'all':[]}

    # The Nutrients we need adding them to the list in the data dictionary
    # Water
    data['all'].append({'name': new2['foodNutrients'][1]['nutrient']['name'], 'amount': (str(new2['foodNutrients'][1]['amount']) + ' ' + str(new2['foodNutrients'][1]['nutrient']['unitName']))})

    # Cholesterol
    data['all'].append({'name': new2['foodNutrients'][66]['nutrient']['name'], 'amount': (str(new2['foodNutrients'][66]['amount']) + ' ' + str(new2['foodNutrients'][66]['nutrient']['unitName']))})

    # Sodium, Na
    data['all'].append({'name': new2['foodNutrients'][15]['nutrient']['name'], 'amount': (str(new2['foodNutrients'][15]['amount']) + ' ' + str(new2['foodNutrients'][15]['nutrient']['unitName']))})

    # Phosphorus
    data['all'].append({'name': new2['foodNutrients'][13]['nutrient']['name'], 'amount': (str(new2['foodNutrients'][13]['amount']) + ' ' + str(new2['foodNutrients'][13]['nutrient']['unitName']))})

    # Sugars, total including NLEA
    data['all'].append({'name': new2['foodNutrients'][8]['nutrient']['name'], 'amount': (str(new2['foodNutrients'][8]['amount']) + ' ' + str(new2['foodNutrients'][8]['nutrient']['unitName']))})

    # Potassium, K
    data['all'].append({'name': new2['foodNutrients'][14]['nutrient']['name'], 'amount': (str(new2['foodNutrients'][14]['amount']) + ' ' + str(new2['foodNutrients'][14]['nutrient']['unitName']))})

    # Protein
    data['all'].append({'name': new2['foodNutrients'][3]['nutrient']['name'], 'amount': (str(new2['foodNutrients'][3]['amount']) + ' ' + str(new2['foodNutrients'][3]['nutrient']['unitName']))})

    # Sending collected data to html
    context = {
        'food' : data
    }

    # Returning a Specific HTML
    return render(request, 'kidney/foodDisplay.html', context)

def FoodTotalPageView(request) :
    # Variables from the Search
    sName = request.GET['name']
    iNumber = request.GET['number']
    iAmount = float(request.GET['amount'])
    iWater = float(request.GET['water'])
    iCholesterol = float(request.GET['cholesterol'])
    iSodium = float(request.GET['sodium'])
    iPhosphorus = float(request.GET['phosphorus'])
    iSugars = float(request.GET['sugars'])
    iPotassium = float(request.GET['potassium'])
    iProtein = float(request.GET['protein'])

    newWater = iAmount * iWater
    newCholesterol = iAmount * iCholesterol
    newSodium = iAmount * iSodium
    newPhosphorus = iAmount * iPhosphorus
    newSugars = iAmount * iSugars
    newPotassium = iAmount * iPotassium
    newProtein = iAmount * iProtein

    new_food = Food()

    new_food.name = sName
    new_food.sodium = newSodium
    new_food.protein = newProtein
    new_food.k = newPotassium
    new_food.phosphorus = newPhosphorus
    new_food.sugar = newSugars
    new_food.cholesterol = newCholesterol
    new_food.water = newWater

    new_food.save()

    id = FoodEntry.objects.latest('foodentryid').foodentryid
    date = FoodEntry.objects.latest('foodentryid').date
    mealType = FoodEntry.objects.latest('foodentryid').mealType

    print(id)
    print(date)
    print(mealType)

    foodEntry = FoodEntry.objects.get(foodentryid=id) # Need to Figure Out Dynamic Pull

    foodEntry.foods.add(new_food)

    api2 = 'https://api.nal.usda.gov/fdc/v1/food/' + str(iNumber) + '?api_key=hzFpuwTYK1oM4XS0SnGp0xJyNVQG7EI4Yq0ZK5dl'

    nutrients = requests.get(api2).json()


    data = {'name': sName, 'number': iNumber, 'amount' : iAmount, 'all':[]}

    data['all'].append({'name': nutrients['foodNutrients'][1]['nutrient']['name'], 'amount': (str(newWater) + ' ' + str(nutrients['foodNutrients'][1]['nutrient']['unitName']))})
    data['all'].append({'name': nutrients['foodNutrients'][66]['nutrient']['name'], 'amount': (str(newCholesterol) + ' ' + str(nutrients['foodNutrients'][66]['nutrient']['unitName']))})
    data['all'].append({'name': nutrients['foodNutrients'][15]['nutrient']['name'], 'amount': (str(newSodium) + ' ' + str(nutrients['foodNutrients'][15]['nutrient']['unitName']))})
    data['all'].append({'name': nutrients['foodNutrients'][13]['nutrient']['name'], 'amount': (str(newPhosphorus) + ' ' + str(nutrients['foodNutrients'][13]['nutrient']['unitName']))})
    data['all'].append({'name': nutrients['foodNutrients'][8]['nutrient']['name'], 'amount': (str(newSugars) + ' ' + str(nutrients['foodNutrients'][8]['nutrient']['unitName']))})
    data['all'].append({'name': nutrients['foodNutrients'][14]['nutrient']['name'], 'amount': (str(newPotassium) + ' ' + str(nutrients['foodNutrients'][14]['nutrient']['unitName']))})
    data['all'].append({'name': nutrients['foodNutrients'][3]['nutrient']['name'], 'amount': (str(newProtein) + ' ' + str(nutrients['foodNutrients'][3]['nutrient']['unitName']))})

    context = {
        'food' : data
    }

    return render(request, 'kidney/foodDisplay.html', context)

# Dashboard Views

def dashboardPageView(request):
    if request.method == 'POST':
        new_date = request.POST.get('date')
        data = LabVitals.objects.filter(personid=1, Date=new_date)
    else:
        data = LabVitals.objects.filter(personid=1)# Need to Figure Out Dynamic Pull

    K_number = 0
    Phos_number = 0
    Na_number = 0
    Creatinine_number = 0
    Albumin_number = 0
    BloodSugar_number = 0
    Weight_number = 0

    iCount = 0

    for datas in data:
        K_number += int(datas.K)
        Phos_number += int(datas.Phos)
        Na_number += int(datas.Na)
        Creatinine_number += int(datas.Creatinine)
        Albumin_number += int(datas.Albumin)
        BloodSugar_number += int(datas.BloodSugar)
        Weight_number += int(datas.Weight)
        
        iCount += 1

    if iCount == 0:
        iCount = 1

    K_total = K_number / iCount
    Phos_total = Phos_number / iCount
    Na_total = Na_number / iCount
    Creatinine_total = Creatinine_number / iCount
    Albumin_total = Albumin_number / iCount
    BloodSugar_total = BloodSugar_number / iCount
    Weight_total = Weight_number / iCount

    context = {
        'data': data,
        'K_number' : K_total,
        'Phos_number' : Phos_total,
        'Na_number' : Na_total,
        'Creatinine_number' : Creatinine_total,
        'Albumin_number' : Albumin_total,
        'BloodSugar_number' : BloodSugar_total,
        'Weight_number' : Weight_total,
    }

    return render(request, 'kidney/dashboard.html', context)

# test

def dashboardMealPageView(request):
    new_date = request.POST.get('date')
    nutrient_type = request.POST.get('nutrient')
    data = FoodEntry.objects.filter(personid=1, date=new_date)  # Need to Figure Out Dynamic Pull

    s_water = 0
    s_sodium = 0
    s_protein = 0
    s_k = 0
    s_phos = 0
    s_sugar = 0
    s_cholesterol = 0

    b_water = 0
    b_sodium = 0
    b_protein = 0
    b_k = 0
    b_phos = 0
    b_sugar = 0
    b_cholesterol = 0

    l_water = 0 
    l_sodium = 0 
    l_protein = 0 
    l_k = 0 
    l_phos = 0 
    l_sugar = 0 
    l_cholesterol = 0 

    d_water = 0
    d_sodium = 0
    d_protein = 0
    d_k = 0
    d_phos = 0
    d_sugar = 0
    d_cholesterol = 0
    
    print(data)
    
    for datas in data:
        print(datas.mealType)

        if datas.mealType == 'snack':
            print(datas.foods.all)
            for f in datas.foods.all() :
                s_water += int(f.water)
                s_sodium += int(f.sodium)
                s_protein += int(f.protein)
                s_k += int(f.k)
                s_phos += int(f.phosphorus)
                s_sugar += int(f.sugar)
                s_cholesterol += int(f.cholesterol)
    
        if datas.mealType == 'breakfast':
            for f in datas.foods.all() :
                b_water += int(f.water)
                b_sodium += int(f.sodium)
                b_protein += int(f.protein)
                b_k += int(f.k)
                b_phos += int(f.phosphorus)
                b_sugar += int(f.sugar)
                b_cholesterol += int(f.cholesterol)

        if datas.mealType == 'lunch':
            for f in datas.foods.all() :
                l_water += int(f.water)
                l_sodium += int(f.sodium)
                l_protein += int(f.protein)
                l_k += int(f.k)
                l_phos += int(f.phosphorus)
                l_sugar += int(f.sugar)
                l_cholesterol += int(f.cholesterol)

        if datas.mealType == 'dinner':
            for f in datas.foods.all() :
                d_water += int(f.water)
                d_sodium += int(f.sodium)
                d_protein += int(f.protein)
                d_k += int(f.k)
                d_phos += int(f.phosphorus)
                d_sugar += int(f.sugar)
                d_cholesterol += int(f.cholesterol)

    snack = {'water' : s_water, 'sodium' : s_sodium, 'protein' : s_protein, 'k' : s_k, 'phos' : s_phos, 'sugar' : s_sugar, 'cholesterol' : s_cholesterol}
    breakfast = {'water' : b_water, 'sodium' : b_sodium, 'protein' : b_protein, 'k' : b_k, 'phos' : b_phos, 'sugar' : b_sugar, 'cholesterol' : b_cholesterol}
    lunch = {'water' : l_water, 'sodium' : l_sodium, 'protein' : l_protein, 'k' : b_k, 'phos' : l_phos, 'sugar' : l_sugar, 'cholesterol' : l_cholesterol}
    dinner = {'water' : b_water, 'sodium' : b_sodium, 'protein' : b_protein, 'k' : b_k, 'phos' : d_phos, 'sugar' : d_sugar, 'cholesterol' : d_cholesterol}

    if nutrient_type == 'water' :
        snack = {'nutrient' : s_water}
        breakfast = {'nutrient' : b_water}
        lunch = {'nutrient' : l_water}
        dinner = {'nutrient' : d_water}
    elif nutrient_type == 'sodium' :
        snack = {'nutrient' : s_sodium}
        breakfast = {'nutrient' : b_sodium}
        lunch = {'nutrient' : l_sodium}
        dinner = {'nutrient' : d_sodium}
    elif nutrient_type == 'protein' :
        snack = {'nutrient' : s_protein}
        breakfast = {'nutrient': b_protein}
        lunch = {'nutrient' : l_protein}
        dinner =  {'nutrient' : l_protein}
    elif nutrient_type == 'k' :
        snack = {'nutrient' : s_k}
        breakfast = {'nutrient' : b_k}
        lunch = {'nutrient' : l_k}
        dinner = {'nutrient' : d_k}
    elif nutrient_type == 'phos' :
        snack = {'nutrient' : s_phos}
        breakfast = {'nutrient': b_phos}
        lunch = {'nutrient' : l_phos}
        dinner = {'nutrient' : l_phos}
    elif nutrient_type == 'sugar' :
        snack = {'nutrient' : s_sugar}
        breakfast = {'nutrient' : b_sugar}
        lunch = {'nutrient' : l_sugar}
        dinner = {'nutrient' : l_sugar}
    elif nutrient_type == 'cholesterol' :
        snack = {'nutrient' : s_cholesterol}
        breakfast = {'nutrient' : b_cholesterol}
        lunch = {'nutrient' : l_cholesterol}
        dinner = {'nutrient' : l_cholesterol}

    print(s_sugar)
    print(b_sugar)
    print(l_sugar)
    print(d_sugar)
    
    context = {
        'data': data,
        'snack' : snack,
        'breakfast' : breakfast,
        'lunch' : lunch,
        'dinner' : dinner,
        'nutrient' : 'water',
    }

    return render(request, 'kidney/dashboardMeal.html', context)

def dashboardNutrientsPageView(request):
    new_date = request.POST.get('date')
    data = FoodEntry.objects.filter(personid=1, date=new_date)  # Need to Figure Out Dynamic Pull

    print(new_date)

    water = 0
    sodium = 0
    protein = 0
    k = 0
    phos = 0
    sugar = 0
    cholesterol = 0
    
    for datas in data:
        for f in datas.foods.all() :
            water += int(f.water)
            sodium += int(f.sodium)
            protein += int(f.protein)
            k += int(f.k)
            phos += int(f.phosphorus)
            sugar += int(f.sugar)
            cholesterol += int(f.cholesterol)

    nutrients = {'water' : water, 'sodium' : sodium, 'protein' : protein, 'k' : k, 'phos' : phos, 'sugar' : sugar, 'cholesterol' : cholesterol}

    context = {
        'data': data,
        'nutrient' : nutrients,
    }

    return render(request, 'kidney/dashboardNutrients.html', context)

# New
def loginPageView(request):
    return render(request, 'kidney/login.html')

def newLoginPageView(request):
    return render(request, 'kidney/newLogin.html')

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been successfully created.")

        return redirect('signin')


    return render(request, "kidney/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "kidney/index.html", {'fName':fname})

        else:
            messages.error(request, "Bad Credentials!")
            return redirect('newLogin')

    return render(request, "kidney/login.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('index')

