from django.shortcuts import get_object_or_404
from .models import Car, Type, User
from .forms import BookingForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout
  # Change: Added import for User model
#from .forms import UserForm, MyUserCreationForm   # CustomerForm  # Change: Added import for UserForm and CustomerForm
from django.core.exceptions import ValidationError
# from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm 
from django.contrib.auth.decorators import login_required
from django.db.models import Q





def home(request):
    query = request.GET.get('q', "") if request.GET.get('q') !=None else ""
    
    cars = Car.objects.filter(
        Q(car_type__name__icontains=query) | 
        Q(model__icontains=query) | 
        Q(make__icontains=query)
    )
    
    types = Type.objects.all()
    
    context = {'cars': cars, 'types': types}
    return render(request, 'base/home.html', context)

# def home(request):
#     cars = Car.objects.all()
    
#     context = {'cars': cars}
    
#     return render (request, 'base/home.html', context) #, context

def car(request, pk):
    car = Car.objects.get(id=int(pk))
    context = {'car': car}
    return render(request, 'base/car.html', context)









def register_page(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username'].lower()  # Ensure username is lowercase
            user.save()
            login(request, user)  # Log in the user after successful registration
            print("User registered successfully:", user.username)  # Debug statement
            return redirect('home')  # Redirect to home or another page upon successful registration
        else:
            print("Form errors:", form.errors)  # Debug statement to see form errors
    else:
        form = UserForm()

    return render(request, 'base/user_registration.html', {'form': form})
    #return render(request, 'base/user_registration.html', {'form': form, 'user_form': user_form})
  






# @login_required(login_url='login')
# def update_user(request):
#     user = request.user
#     form = UserForm(instance=user)

#     if request.method == "POST":
#         form = UserForm(request.POST, instance=user)  #request.FILES
#         if form.is_valid():
#             form.save()
#             return redirect('user-profile', pk=user.id)  

#     return render(request, "base/update-user.html", {'form': form})


@login_required(login_url='login')
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserUpdateForm(instance=user)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('home')  # Redirect to the home page after successful update

    return render(request, "base/update_user.html", {'form': form})






from .forms import BookingForm  # Assuming you have a form for booking input

@login_required
def create_booking(request, car_id):
    car = Car.objects.get(pk=car_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            try:
                booking.clean()  # Validate availability
            except ValidationError as e:
                form.add_error(None, e)
                return render(request, 'bookings/booking_form.html', {'form': form})

            booking.save()
            return redirect('booking_success')  # Redirect to a success page or view
    else:
        form = BookingForm(initial={'car': car})
    
    return render(request, 'bookings/booking_form.html', {'form': form})



from django.shortcuts import render
from .models import Car

def available_cars(request):
    # Retrieve available cars logic goes here
    cars = Car.objects.filter(is_available=True)  # Example logic to filter available cars

    context = {
        'cars': cars
    }
    return render(request, 'base/available_cars.html', context)



# def book_car(request, car_id):
#     car = get_object_or_404(Car, pk=car_id)
#     # Additional logic for booking the car can go here
#     return render(request, 'base/book_car.html', {'car': car})


# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from .models import Car

# def book_car(request, car_id):
#     car = get_object_or_404(Car, pk=car_id)
#     if request.method == 'POST':
#         # Process booking logic here
#         return HttpResponse("Booking successful!")  # Replace with appropriate response
    
#     return render(request, 'base/book_car.html', {'car': car})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Car, Booking
from .forms import BookingForm
def book_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Assuming the user is logged in
            booking.car = car
            try:
                booking.clean()
                booking.save()
                messages.success(request, 'You have booked the car successfully!')
                return redirect('')  # Redirect to the home page
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = BookingForm()

    return render(request, 'base/book_car.html', {'car': car, 'form': form})


# @login_required(login_url='login') es bolo
# def update_user(request, pk):
#     user = get_object_or_404(User, pk=pk)  # Fetch the user object based on pk
#     form = UserUpdateForm(instance=user)

#     if request.method == "POST":
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('home', pk=user.pk)  # Redirect to user profile page

#     return render(request, "base/update_user.html", {'form': form})



# @login_required(login_url='login')
# def update_user(request, pk):
#     user = get_object_or_404(User, pk=pk)  # Fetch the user object based on pk
    
#     if request.method == "POST":
#         form = UserUpdateForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user-profile', pk=user.pk)  # Redirect to user profile page
#     else:
#         form = UserUpdateForm(instance=user)  # Initialize the form with the user instance

#     return render(request, "base/update_user.html", {'form': form})



# @login_required
# def update_user(request, pk):
#     user = get_object_or_404(User, pk=pk)
  
    
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=user)
#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             if 'password' in user_form.cleaned_data and user_form.cleaned_data['password']:
#                 user.set_password(user_form.cleaned_data['password'])
#             user.save()

            
#             user = user()
           

#             return redirect('home')
#         else:
#             print("User form errors:", user_form.errors)
           
#     else:
#         user_form = UserForm(instance=user)
        
    
#     context = {'user_form': user_form, 'user_form': user_form}
#     return render(request, 'base/user_registration.html', context)





def logout_view(request):
    logout(request)
    return redirect('home')

# def register_page(request):
#     form = MyUserCreationForm()
#     if request.method == "POST":
#         form = MyUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             login(request, user)
#             return redirect('home')
#     return render(request, 'base/user_registration_old.html', {'form': form})

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username doesn't exist")
            return render(request, 'base/login.html', {})
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect")
      
    context  = {}
    
    return render(request, 'base/login.html', context)
  






# def home(request):
#     query = request.GET.get('q', "")
    
#     cars = Car.objects.filter(
#         Q(car_type__name__icontains=query) | 
#         Q(model__icontains=query) | 
#         Q(make__icontains=query)
#     )
    
#     types = Type.objects.all()
    
#     context = {'cars': cars, 'types': types}
#     return render(request, 'base/home.html', context)

# Create your views here.
