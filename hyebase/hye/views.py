from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from hye.forms import loginForm, ProfileForm
from hye.models import Profile, Follow
from django.contrib import messages

# Or query in SQL
from django.db.models import Q


class loginUser(View):
    '''Authenticates the user'''
    
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/main/')
        else:
            return render_to_response('registration/login.html', {'form':loginForm}, context_instance=RequestContext(request))
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/main/')
            
        
        else:
            error = "Username or Password incorrect"
            return render_to_response('registration/login.html', {'error':error, 'form':loginForm}, context_instance=RequestContext(request))


class main(View):
    def get(self, request):
        
        # Check whether the user have already created profile or not.
        exist = Profile.objects.filter(user_id=request.user.id)
        
        if exist:
            return HttpResponseRedirect('/showProfile/')
        
        else:
            return render_to_response('index.html', {'form':ProfileForm}, context_instance=RequestContext(request))
        
        
class createProfile(View):
    '''Create a Profile'''
    
    def post(self, request):
        # Get all the data from form
        
        form = ProfileForm(request.POST)
        
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        
        
        location = request.POST['location']
        interest = request.POST['interest']
        contact = request.POST['contact']
        email = request.POST['email']
        
        
        # Check whether email is taken or not
        email = Profile.objects.filter(email=email)
        
        if email:
            state = "Email is already taken"
            return render_to_response('index.html', {'state':state}, context_instance=RequestContext(request))
        
        
        try:
            p = Profile(user_id=request.user.id, firstname=firstname, lastname=lastname, email=email,
                        location=location, interest=interest, contact=contact)
            p.save()
            return HttpResponseRedirect('/showProfile/')
            #else:
            return render_to_response('index.html', {'form':ProfileForm}, context_instance=RequestContext(request))
        except:
            return HttpResponseRedirect('/showProfile/')
        
        # Inserts into the database
        
class showProfile(View):
    def get(self, request):
        profile = Profile.objects.filter(user_id=request.user.id)
        
        # Find the users who are followed my the logged in user
        
        followed_users = Follow.objects.filter(user_id=request.user.id)
        followed = [i.followed_user for i in followed_users]
        
        
        followed_users_template = Profile.objects.filter(user_id__in=followed)
        first_name = [i.firstname for i in followed_users_template]
        last_name = [i.lastname for i in followed_users_template]
        id_followed = [i.user_id for i in followed_users_template]
           
        users = zip(first_name, last_name, id_followed)
        
        # Find the users which are following the logged in user
        
        followed_users = Follow.objects.filter(followed_user=request.user.id)
        followed = [i.user_id for i in followed_users]
        
        
        followed_users_template = Profile.objects.filter(user_id__in=followed)
        first_name = [i.firstname for i in followed_users_template]
        last_name = [i.lastname for i in followed_users_template]
        id_followed = [i.user_id for i in followed_users_template]
           
        following = zip(first_name, last_name, id_followed)
        
        

        return render_to_response('show_profile.html', {'following':following, 'edit':'edit', 'profile':profile, 'users':users}, context_instance=RequestContext(request))
        
        
        
    def post(self, request):
        
        user_id = request.POST['id_followed_user']
        profile = Profile.objects.filter(user_id=user_id)
        
        # Find the users who are followed my the logged in user
        
        followed_users = Follow.objects.filter(user_id=request.user.id)
        followed = [i.followed_user for i in followed_users]
        
        
        followed_users_template = Profile.objects.filter(user_id__in=followed)
        first_name = [i.firstname for i in followed_users_template]
        last_name = [i.lastname for i in followed_users_template]
        id_followed = [i.user_id for i in followed_users_template]
           
        users = zip(first_name, last_name, id_followed)
        
        # Find the users which are following the logged in user
        
        followed_users = Follow.objects.filter(followed_user=request.user.id)
        followed = [i.user_id for i in followed_users]
        
        
        followed_users_template = Profile.objects.filter(user_id__in=followed)
        first_name = [i.firstname for i in followed_users_template]
        last_name = [i.lastname for i in followed_users_template]
        id_followed = [i.user_id for i in followed_users_template]
           
        following = zip(first_name, last_name, id_followed)

        return render_to_response('show_profile.html', {'following':following, 'profile':profile, 'users':users}, context_instance=RequestContext(request))

class updateProfile(View):
    
    
    def get(self, request):
        button_name = request.GET['button-name']
        
        if button_name == 'search':
            # Do our search thing
            search_input = request.GET['search_input']
        
            # Search using first, name and email address on Profile model
            
            p = Profile.objects.filter(Q(firstname__contains=search_input) | Q(lastname__contains=search_input) | Q(email=search_input)).exclude(user_id=request.user.id)
            # Show with first_name + last_name --> also send user_ id to show in later user
            first_name = [i.firstname for i in p]
            last_name = [i.lastname for i in p]
           
            get_user_id = [i.user_id for i in p]
            full_name= zip(first_name, last_name, get_user_id)
            
            email = [i.email for i in p]
            email_and_id = zip(email, get_user_id)
            state = "No user with that name or email."
            
            # If no search result
            if len(p) == 0:
                return render_to_response('search_result.html', {'state':state}, context_instance=RequestContext(request))
            
            
            # If search results
            else:
                return render_to_response('search_result.html', {'full_name':full_name}, context_instance=RequestContext(request))
        

                
        else:
            firstname = request.GET['firstname']
            lastname = request.GET['lastname']
            location = request.GET['location']
            interest = request.GET['interest']
            contact = request.GET['contact']
            email = request.GET['email']
            Profile.objects.filter(user_id=request.user.id).update(firstname=firstname, lastname=lastname, location=location,
                                                                   interest=interest, contact=contact, email=email)
            
            messages.success(request, 'Profile successfully updated')
            return HttpResponseRedirect('/main/')

class followUsers(View):
    def post(self, request):
        followed_user = request.POST['follow_id']     
        
        # Check if user is already followed
        f = Follow.objects.filter(user_id=request.user.id, followed_user=followed_user)
        if f:
            messages.error(request, 'You have already followed that user.')
            return HttpResponseRedirect('/main/')
 
        else:
            b = Follow(user_id=request.user.id, followed_user=followed_user)
            b.save()
            messages.success(request, 'Successfully followed')
            return HttpResponseRedirect('/main/')
        
