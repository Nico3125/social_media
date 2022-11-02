import random
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from .forms import NewEventForm
from .models import Event
from .models import Profile, FriendRequest


def index(request):
    return render(request, 'index.html')


def inregistrare(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cont inregistrat pentru {username}!')
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'posts/inregistrare.html', context)


def login(request):
    context = {}
    return render(request, 'posts/login.html', context)


User = get_user_model()


@login_required
def my_profile(request):
    p = request.user.profile
    you = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=you)
    rec_friend_requests = FriendRequest.objects.filter(to_user=you)
    user_events = Event.objects.filter(author=you)
    friends = p.friends.all()

    # is this user our friend
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        # if we have sent him a friend request
        if FriendRequest.objects.filter(
                from_user=request.user).filter(to_user=you).count()==1:

            button_status = 'friend_request_sent'

        if len(FriendRequest.objects.filter(
                from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'friend_request_received'

    context = {
        'u': you,
        'button_status': button_status,
        'friend_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests,
        'events_count': user_events.count
    }

    return render(request, 'posts/profile.html', context)




@login_required
def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    sent_to = []
    friends = []
    for user in users:
        friend = user.friends.all()
        for f in friend:
            if f in friends:
                friend = friend.exclude(user=f.user)
        friends += friend
    my_friends = request.user.profile.friends.all()
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    if request.user.profile in friends:
        friends.remove(request.user.profile)
    random_list = random.sample(list(users), min(len(list(users)), 10))
    for r in random_list:
        if r in friends:
            random_list.remove(r)
    friends += random_list
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    for se in sent_friend_requests:
        sent_to.append(se.to_user)
    context = {
        'users': friends,
        'sent': sent_to
    }
    return render(request, "users_list.html", context)


def friend_list(request):
    p = request.user.profile
    friends = p.friends.all()
    context = {
        'friend_list': friends
    }
    return render(request, "post/friend_list.html", context)


@login_required
def send_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user)
    return HttpResponseRedirect(f'posts/{user.profile.slug}')


@login_required
def cancel_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(
        from_user=request.user,
        to_user=user).first()
    frequest.delete()
    return HttpResponseRedirect(f'posts/{user.profile.slug}')


@login_required
def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    if (FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
        request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()
        request_rev.delete()
    frequest.delete()
    return HttpResponseRedirect(f'posts/{request.user.profile.slug}')


@login_required
def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect(f'posts/{request.user.profile.slug}')

#
# @login_required
# def delete_friend(request, id):
#     user_profile = request.user.profile
#     friend_profile = get_object_or_404(Profile, id=id)
#     user_profile.friends.remove(friend_profile)
#     friend_profile.friends.remove(user_profile)
#     return HttpResponseRedirect(f'posts/{friend_profile.slug}')


@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    # print(p)
    u = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
    user_events = Event.objects.filter(user=u)

    friends = p.friends.all()

    # is this user our friend
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        # if we have sent him a friend request
        if len(FriendRequest.objects.filter(
                from_user=request.user).filter(to_user=p.user)) == 1:
            button_status = 'friend_request_sent'

        # if we have recieved a friend request
        if len(FriendRequest.objects.filter(
                from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'friend_request_received'

    context = {
        'u': u,
        'button_status': button_status,
        'friend_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests,
        'events_count': user_events.count
    }

    return render(request, "profile.html", context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Contul tau este la zi!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'posts/edit_profile.html', context)


@login_required
def search_users(request):
    query = request.GET.get('q')
    object_list = User.objects.filter(username__icontains=query)
    context = {
        'events': object_list
    }
    return render(request, "search_events.html", context)


# class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
#     template_name = 'registration/password_reset_file.html'
#     email_template_name = 'registration/password-reset-email.html'
#     subject_template_name = 'registration/password-reset-subject.txt'
#     success_message = "Ai primit un email cu instructiuni pentru resetarea parolei. " \
#                       "Daca exista un cont asociat adresei introduse de tine vei primi mesajul in scurt timp." \
#                       " Daca nu primesti niciun email, " \
#                       "te rugam verifica daca ai introdus corect adresa ta de mail si verifica folderul spam."
#     success_url = reverse_lazy('profile')


intalniri = [
    {'Title': 'Hai la joaca!',
     'Autor': 'Nicoleta',
     'Nume': 'Catalin',
     'Varsta': '1 an',
     'Data': '10.10.2020',
     'Ora': '11:00',
     'Locatia': 'Un loc pe harta',

     },
    {'Autor': 'Nicoleta',
     'Nume': 'Lorelai',
     'Varsta': '4 ani',
     'Data': '10.10.2020',
     'Ora': '11:00',
     'Locatia': 'Un loc pe harta',

     }
]


def home(request):
    context = {
        'intalniri': intalniri,
    }
    return render(request, 'posts/home.html', context)


def about(request):
    return render(request, 'posts/about.html')


class EventListView(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'events'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        #     liked = [i for i in Event.objects.all() if Like.objects.filter(user=self.request.user, post=i)]
        #     context['liked_post'] = liked
        return context


class UserEventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'user_events.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(UserEventListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, user=self.kwargs.get('username'))
        return context


def get_queryset(self):
    user = get_object_or_404(User, user=self.kwargs.get('username'))
    return Event.objects.filter(author_id=user).order_by('-date_posted')


# @login_required
# def event_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     user = request.user
#
#     if request.method == 'POST':
#         form = NewCommentForm(request.POST)
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.post = post
#             data.username = user
#             data.save()
#             return redirect('post-detail', pk=pk)
#     else:
#         form = NewCommentForm()
#     return render(request, 'feed/post_detail.html', {'post': post, 'is_liked': is_liked, 'form': form})


@login_required
def create_event(request):
    user = request.user
    if request.method == "POST":
        form = NewEventForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_name = user
            data.save()
            messages.success(request, f'Intalnire creeata!')
            return redirect('home')
    else:
        form = NewEventForm()
    return render(request, 'create_event.html', {'form': form})


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'location', 'author', 'nume', 'varsta' ]
    template_name = '/create_event.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False


@login_required
def event_delete(request, pk):
    event = Event.objects.get(pk=pk)
    if request.user == event.user_name:
        Event.objects.get(pk=pk).delete()
    return redirect('home')


@login_required
def search_events(request):
    query = request.GET.get('q')
    object_list = Event.objects.filter(title__icontains=query)
    context = {
        'events': object_list,

    }
    return render(request, "search_events.html", context)
