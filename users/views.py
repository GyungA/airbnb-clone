import os
import requests
from django.views.generic import FormView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from . import forms, models


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def LogoutView(request):
    messages.info(request, f"See you later See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)

                if username is not None:
                    name = profile_json.get("name")
                    if name is None:
                        name = username
                    email = profile_json.get("email")
                    if email is None:
                        email = name
                    bio = profile_json.get("bio")
                    if bio is None:
                        bio = ""
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please login in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


# def kakao_login(request):
#     client_id = os.environ.get("KAKAO_ID")
#     redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
#     return redirect(
#         f"https://kauth.kakao.com/oaut/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
#     )


# class KakaoExcpetion(Exception):
#     pass


# def kakao_callback(request):
#     try:
#         code = request.GET.get("code")
#         client_id = os.environ.get("KAKAO_ID")
#         redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
#         token_request = requests.get(
#             f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
#         )
#         token_json = token_request.json()
#         error = token_json.get("error", None)
#         if error is not None:
#             raise KakaoExcpetion("Can't get authorization code.")
#         access_token = token_json.get("access_token")
#         profile_request = requests.get(
#             "https://kapi.kakao.com/v1/user/me",
#             headers={"Authorization": f"Bearer {access_token}"},
#         )
#         profile_json = profile_request.json()
#         email = profile_json.get("kaccount_email", None)
#         if email is None:
#             raise KakaoExcpetion("Please also give me your email")
#         properties = profile_json.get("properties")
#         nickname = properties.get("nickname")
#         profile_image = properties.get("profile_image")
#         try:
#             user = models.User.objects.get(email=email)
#             if user.login_method != models.User.LOGING_KAKAO:
#                 raise KakaoExcpetion(f"Please log in with: {user.login_method}")
#         except models.User.DoesNotExist:
#             user = models.User.objects.create(
#                 email=email,
#                 username=email,
#                 first_name=nickname,
#                 login_method=models.User.LOGING_KAKAO,
#                 email_verified=True,
#             )
#             user.set_unusable_password()
#             user.save()
#             if profile_image is not None:
#                 phto_request = requests.get(profile_image)
#                 user.avatar.save(
#                     f"{nickname}-avatar", ContentFile(phto_request.content)
#                 )
#         messages.success(request, f"Welcome back {user.first_name}")
#         login(request, user)
#         return redirect(reverse("core:home"))
#     except KakaoExcpetion as e:
#         messages.error(request, e)
#         return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"
