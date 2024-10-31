import requests
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from py_mssso import MSSSOHelper

# Create your views here.


_LOGIN_FAIL_URL = "/"
_LOGIN_SUCCESS_URL = "/"
_MSGRAPH_BASE_URI = "https://graph.microsoft.com/v1.0"
_MSGRAPH_QUERY_SELECT_ITEMS_FOR_USER = ",".join(
    [
        # "displayName",
        "givenName",
        "surname",
        "mail",
        # "mobilePhone",
        # "officeLocation",
        "userPrincipalName",
        # "jobTitle",
        # "department",
        # "companyName",
        # "onPremisesSamAccountName",
    ]
)


# sso login
def sso_login(request):
    if not request.session.session_key:
        request.session.create()
    msal_flow = MSSSOHelper.get().get_auth_code_flow()
    request.session["msal_flow"] = msal_flow
    request.session.save()
    return HttpResponseRedirect(msal_flow.get("auth_uri"))


# django login helper
def _login(request, username):
    try:
        user = get_user_model().objects.get(username=username, is_active=True)
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
    except:
        raise Exception(f"Login Failed - user not exist: [{username}]")


def sso_login_callback(request):
    msal_flow = request.session.get("msal_flow")

    try:
        # get token
        token = MSSSOHelper.get().get_token(
            auth_code_flow=msal_flow,
            auth_res=request.GET,
        )

        # set request header
        headers = {"Authorization": f"Bearer {token}"}

        # get user data with MS Graph API
        res_user = requests.get(
            f"{_MSGRAPH_BASE_URI}/me?$select={_MSGRAPH_QUERY_SELECT_ITEMS_FOR_USER}",
            headers=headers,
        )

        ms_user_obj = res_user.json()
        username = ms_user_obj.get("userPrincipalName")
        if not username:
            raise Exception("Invalid User")

        # create or update django user
        get_user_model().objects.update_or_create(
            username=username,
            defaults={
                "first_name": ms_user_obj.get("givenName"),
                "last_name": ms_user_obj.get("surname"),
                "email": ms_user_obj.get("mail"),
                "is_active": True,
            },
        )

        # django login
        _login(request, username)
    except:
        return HttpResponseRedirect(_LOGIN_FAIL_URL)

    return HttpResponseRedirect(_LOGIN_SUCCESS_URL)


def index(request):
    context = {}
    return HttpResponse(render(request, "home.html", context))


def logout_view(request):
    # django logout
    logout(request)
    return HttpResponseRedirect("/")
