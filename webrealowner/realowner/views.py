from django.shortcuts import render, redirect ,get_object_or_404
from .models import Item ,UserProfile
from django.shortcuts import get_object_or_404
from .forms import ItemForm, UserProfileForm ,EmailUpdateForm ,ContactChannelsForm,UserRegistrationForm,f,ItemEditForm,TransferItemForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.templatetags.static import static
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseForbidden
from django.contrib.auth import views as auth_views
from django.db.models import Count 
# Create your views here.



def home(request):
    items = Item.objects.all()
    search_query = request.GET.get('search')

    if search_query:
        items = items.filter(model__icontains=search_query)

    context = {
        'items': items,
    }
    return render(request, 'registration/home.html', context)

class LoginView(auth_views.LoginView):
    template_name = 'login.html'  
    redirect_authenticated_user = True  

    def get_success_url(self):
        
        return self.get_redirect_url() or 'registration/login.html'


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        forms = UserProfileForm(request.POST,request.FILES)
        if form.is_valid() and forms.is_valid():
            users=form.save(commit=False) 
            users.save() 
            forms.save(commit=False).user=users
            forms.save() 
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
        forms = UserProfileForm()
    return render(request, 'registration/register.html', {'form': form,'forms':forms})



def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    owned_items_count = Item.objects.filter(current_owner=profile).aggregate(total_items=Count('id'))['total_items']

    context = {
        'user': user,
        'profile': profile,
        'owned_items_count': owned_items_count  
    }

    return render(request, 'registration/profile.html', context)


@login_required
def create_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile') 
    else:
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
    return render(request, 'edit/create_profile.html', {'form': form, 'profile': profile})

@login_required
def create_item(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.current_owner = user_profile
            item.save()
            form.save_m2m()  

            messages.success(request, 'Your item has been posted!')
            return redirect('item_list', ct=item.category.name if item.category else '')
    else:
        form = ItemForm()

    return render(request, 'app/create_item.html', {'form': form})


@login_required
def item_list(request, ct):
    user_profile = UserProfile.objects.get(user=request.user)

    if ct:
        items = Item.objects.filter(category__name=ct, current_owner=user_profile).order_by('-store_date_of_purchase')
    else:
        items = Item.objects.filter(current_owner=user_profile).order_by('-store_date_of_purchase') 

    return render(request, 'app/item-list.html', {'items': items, 'ct': ct})


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.current_owner = user_profile
            item.save()
            form.save_m2m()

            messages.success(request, 'Your item has been updated!')
            return redirect('item_list', ct=item.category.name if item.category else '')
    else:
        form = ItemForm(instance=item)

    return render(request, 'edit/edit_item.html', {'form': form, 'item': item})





@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id, owner=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Your item has been deleted.')
        return redirect('item_list')
    return render(request, 'app/delete_item.html', {'item': item})


def edit_password(req):
    if req.method == 'POST':
        form = PasswordChangeForm(req.user, req.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(req, user)
            messages.success(req, 'รหัสผ่านของคุณถูกเปลี่ยนแล้ว!')
            return redirect('edit_password')
        else:
            messages.error(req, 'กรุณาแก้ไขข้อผิดพลาดด้านล่าง')
    else:
        form = PasswordChangeForm(req.user)

    context = {'form': form}
    return render(req, 'edit/edit_password.html', context)


@login_required
def edit_email(request):
    if request.method == 'POST':
        form = EmailUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email has been updated.')
            return redirect('create_profile')
    else:
        form = EmailUpdateForm(instance=request.user)
    
    return render(request, 'edit/edit_email.html', {'form': form})


@login_required
def edit_contact_channels(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)  

    if request.method == 'POST':
        form = ContactChannelsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your contact channels have been updated.')
            return redirect('create_profile')
    else:
        form = ContactChannelsForm(instance=profile)

    return render(request, 'edit/edit_contact_channels.html', {'form': form})



@login_required
def edit_personal_details(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    
    if request.method == 'POST':
        profile_form = f(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your personal details have been updated.')
            return redirect('create_profile')  
    else:
        profile_form = f(instance=profile)

    return render(request, 'edit/edit_personal_details.html', {'profile_form': profile_form})



@login_required
def edit_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit/edit_profile.html', {'form': form})


@login_required
def transfer_item(request):
    if request.method == 'POST':
        form = TransferItemForm(request.POST)
        if form.is_valid():
            item_serial_number = form.cleaned_data['item_serial_number']
            new_owner_username = form.cleaned_data['new_owner_username']

            item = get_object_or_404(Item, serial_number=item_serial_number)
            new_owner = get_object_or_404(UserProfile, user__username=new_owner_username)

            if item.current_owner != request.user.userprofile:
                messages.error(request, "You are not the current owner of this item.")
                return redirect('transfer_item')

            item.previous_owners.add(item.current_owner)
            item.current_owner = new_owner
            item.save()
            
            
            profile = request.user.userprofile
            profile.transferred_items_count += 1
            profile.save()

            messages.success(request, f"Item '{item.serial_number}' has been transferred to {new_owner.user.username}.")
            return redirect('transfer_item')
        
    else:
        form = TransferItemForm()

    return render(request, 'app/transfer_item.html', {'form': form})
