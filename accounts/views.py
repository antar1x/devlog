from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, TemplateView

from accounts.forms import RegisterForm, SearchForm
from logs.models import LogSession, Topic, Goal


class CustomLoginView(LoginView):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

        return render(request, 'account/login.html', {'form': form})


class UserRegistrationView(CreateView):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
        else:
            return render(request, 'account/register.html', {'form': form})


class HomeView(TemplateView):
    def get(self, request):
        return render(request, 'home.html')

class ProfileView(View):

    def get(self, request):
        form = SearchForm()
        return render (request, 'profile_search.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                if user.profile.is_public:
                    sessions = LogSession.objects.filter(user=user)

                    total_minutes = sessions.aggregate(
                        total=Sum('duration_minutes')
                    )['total'] or 0

                    total_hours = total_minutes / 60

                    total_topics = Topic.objects.filter(user=user).count()

                    last_5_sessions = sessions.select_related('topic').order_by('-date')[:5]

                    goals = Goal.objects.filter(user=user).select_related('topic')
                    return render(
                        request,
                        "public_profile.html",
                        {
                            "profile": user.profile,
                            "total_minutes": total_minutes,
                            "total_hours": total_hours,
                            "total_topics": total_topics,
                            "last_5_sessions": last_5_sessions,
                            "goals": goals,
                        }
                    )
                return render(
                    request,
                    "profile_search.html",
                    {
                        "form": form,
                        "error": "Profile is not public"
                    }
                )
            except User.DoesNotExist:

                return render(request, "profile_search.html", {"form": form,
                                                     "error": "User not found"})

        return render(
            request,
            "profile_search.html",
            {"form": form}
        )

class PublicProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)

        if not user.profile.is_public:
            raise Http404

        sessions = LogSession.objects.filter(user=user)

        total_minutes = sessions.aggregate(
            total=Sum('duration_minutes')
        )['total'] or 0

        total_hours = total_minutes / 60

        total_topics = Topic.objects.filter(user=user).count()

        last_5_sessions = sessions.select_related('topic').order_by('-date')[:5]

        goals = Goal.objects.filter(user=user).select_related('topic')

        return render(request, 'account/public_profile_by_id.html', {
            'profile': user.profile,
            'total_minutes': total_minutes,
            'total_hours': total_hours,
            'total_topics': total_topics,
            'last_5_sessions': last_5_sessions,
            'goals': goals,
        })
