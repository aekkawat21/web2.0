from django.shortcuts import render, redirect ,get_object_or_404
from .models import Item ,UserProfile
from .forms import ItemForm, UserProfileForm ,EmailUpdateForm ,ContactChannelsForm,UserRegistrationForm,EditPersonalDetailsForm,TransferItemForm,ItemEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.templatetags.static import static
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.db.models import Count 
from django.contrib.auth.models import User

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
        if form.is_valid() : 
            users=form.save(commit=False) 
            users.save() 
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
       
        
    return render(request, 'registration/register.html', {'form':form})


def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Count items currently owned by the user
    owned_items_count = Item.objects.filter(current_owner=profile).count()
    
    # Count items transferred by the user
    transferred_items_count = Item.objects.filter(previous_owners=profile).exclude(current_owner=profile).count()

    context = {
        'user': user,
        'profile': profile,
        'owned_items_count': owned_items_count,
        'transferred_items_count': transferred_items_count
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

    previous_owners = item.previous_owners.all()
    print("Previous owners in view:")
    for owner in previous_owners:
        print(owner.user.username)  # Assuming UserProfile has a ForeignKey to User

    if request.method == 'POST':
        form = ItemEditForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            form.save_m2m()

            messages.success(request, 'Your item has been updated!')
            return redirect('item_list', ct=item.category.name if item.category else '')
    else:
        form = ItemEditForm(instance=item)
        previous_owners = item.previous_owners.all()  # Ensure previous owners are available for the template

    return render(request, 'edit/edit_item.html', {'form': form, 'item': item, 'previous_owners': previous_owners})


@login_required
def transfer_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    current_user_profile = request.user.userprofile
    
    if request.method == 'POST':
        form = TransferItemForm(request.POST)
        if form.is_valid():
            new_owner_name = form.cleaned_data['new_owner_username']
            print(f"New owner username: {new_owner_name}")  # Debugging print
            new_owner_user = get_object_or_404(User, username=new_owner_name)
            new_owner_profile = get_object_or_404(UserProfile, user=new_owner_user)
            
            if item.current_owner != current_user_profile:
                messages.error(request, "You are not the current owner of this item.")
                return redirect('item_list_no_ct')
            
            # Add the current owner to the previous_owners
            if item.current_owner:
                print(f"Adding current owner to previous owners: {item.current_owner.user.username}")  # Debugging print
                item.previous_owners.add(item.current_owner)
            
            # Update the current_owner to the new owner
            item.current_owner = new_owner_profile
            item.save()
            
            print(f"Item transferred to: {new_owner_profile.user.username}")  # Debugging print
            messages.success(request, "Item successfully transferred.")
            return redirect('item_list_no_ct')
    else:
        form = TransferItemForm()

    return render(request, 'app/transfer_item.html', {'form': form, 'item': item})



@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id, owner=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Your item has been deleted.')
        return redirect('item_list')
    return render(request, 'app/delete_item.html', {'item': item})


@login_required
def edit_password(req):
    if req.method == 'POST':
        form = PasswordChangeForm(req.user, req.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(req, user)
            messages.success(req, 'รหัสผ่านของคุณถูกเปลี่ยนแล้ว!')
            return redirect('create_profile')
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
        profile_form = EditPersonalDetailsForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your personal details have been updated.')
            return redirect('create_profile')  
    else:
        profile_form = EditPersonalDetailsForm(instance=profile)

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
            return redirect('create_profile') 
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit/edit_profile.html', {'form': form})

