from django.contrib.auth.models import User
from rest_framework import status

from LILAGameAPI.base_api_views import GlobalAPIView
from LILAGameAPI.standard_responses import StandardResponse
from LILAGameAPI.utils import required_params
from user_auth.serializers import UserSerializer
from user_auth.utils import validate_user_password


class RegisterView(GlobalAPIView):
    @required_params(params=["username", "email", "password", "first_name"])
    def post(self, request):
        data = request.data
        errors = {}
        username = data.get("username")
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")

        if not username:
            errors.update({"username": "Username is mandatory"})

        if not email:
            errors.update({"email": "Email is mandatory"})

        if not password:
            errors.update({"password": "Password is mandatory"})

        if not first_name:
            errors.update({"first_name": "First name is mandatory"})

        if username and User.objects.filter(username__iexact=username).exists():
            errors.update({"username": "Username already exists"})

        if email and User.objects.filter(email__iexact=email).exists():
            errors.update({"email": "Email already exists"})

        if errors:
            return StandardResponse(
                response_data={},
                error=errors,
                http_status=status.HTTP_400_BAD_REQUEST,
                message="Error while registering new user",
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        serialized_data = UserSerializer(user).data
        message = "Successfully registered a user"
        return StandardResponse(response_data=serialized_data, message=message)


class LoginView(GlobalAPIView):
    @required_params(params=["username", "password"])
    def post(self, request):
        data = request.data
        errors = {}
        username = data.get("username")
        password = data.get("password")

        if not username:
            errors.update({"username": "Username is mandatory"})

        if username and not User.objects.filter(username__iexact=username).exists():
            errors.update({"username": "Username does not exists"})

        if not password:
            errors.update({"password": "Password is mandatory"})

        if errors:
            return StandardResponse(
                response_data={},
                error=errors,
                http_status=status.HTTP_400_BAD_REQUEST,
                message="Error with user login",
            )

        user = validate_user_password(username=username, password=password)

        if not user:
            return StandardResponse(
                response_data={},
                http_status=status.HTTP_400_BAD_REQUEST,
                message="Username or password not valid",
            )

        serialized_data = UserSerializer(user).data
        message = "Successfully logged in"
        return StandardResponse(response_data=serialized_data, message=message)
