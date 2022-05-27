from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from LILAGameAPI.base_api_views import GlobalAPIView
from LILAGameAPI.standard_responses import StandardResponse
from LILAGameAPI.utils import required_params
from user_auth.serializers import UserSerializer
from user_auth.utils import validate_user_password


class RegisterView(GlobalAPIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            operation_description="To register as new user",
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Username of the user. Mandatory field",
                ),
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Email of the user. Mandatory field",
                ),
                "first_name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="First name of the user. Mandatory field",
                ),
                "last_name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Last name of the user. Optional field",
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Password of the user. Mandatory field",
                ),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "pk": openapi.Schema(
                        type=openapi.TYPE_STRING, description="PK of User"
                    ),
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Username of the User"
                    ),
                    "first_name": openapi.Schema(
                        type=openapi.TYPE_STRING, description="First name of the User"
                    ),
                    "last_name": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Last name of the User"
                    ),
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Email of the user"
                    ),
                    "token": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Token for using on all authenticated APIs",
                    ),
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="If username already exists or not provided",
                    ),
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="If email already exists or not provided",
                    ),
                    "first_name": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="If first name not provided",
                    ),
                    "password": openapi.Schema(
                        type=openapi.TYPE_STRING, description="If password not provided"
                    ),
                },
            ),
        },
    )
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
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            operation_description="Allow user to login",
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Username of the user. Mandatory field",
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Password of the user. Mandatory field",
                ),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "pk": openapi.Schema(
                        type=openapi.TYPE_STRING, description="PK of User"
                    ),
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Username of the User"
                    ),
                    "first_name": openapi.Schema(
                        type=openapi.TYPE_STRING, description="First name of the User"
                    ),
                    "last_name": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Last name of the User"
                    ),
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Email of the user"
                    ),
                    "token": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Token for using on all authenticated APIs",
                    ),
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="If username does not exists or not provided",
                    ),
                    "password": openapi.Schema(
                        type=openapi.TYPE_STRING, description="If password not provided"
                    ),
                },
            ),
        },
    )
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
