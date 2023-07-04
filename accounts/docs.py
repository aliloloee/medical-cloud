from drf_yasg import openapi


schemas = {
    'RegisterAPISchema' : dict(
        operation_description='Register a new user or Retrieve informations of a verified user',
        operation_summary="Create a new user",
        responses={
            "201": openapi.Response(
                description="user created",
                examples={
                    "application/json": {
                        "id": 0,
                        "email": "string",
                        "firstname": "string",
                        "lastname": "string"
                    }
                }
            ),
            "403": openapi.Response(
                description="Authenticated user is not allowed to register new user",
            ),
        }
    ),

    'VerifyAPISchema' : dict(
        operation_description='Activate the new user in the system and return related auth tokens',
        operation_summary='Verify a new user',
        responses={
            "200": openapi.Response(
                description="User activated",
                examples={
                    "application/json": {
                        "refresh": "string",
                        "access": "string",
                    }
                }
            )
        }
    ),

    'PasswordChangeAPISchema' : dict(
        operation_description='Changing password of logged in user',
        operation_summary='Changing password',
        responses={
            "200": openapi.Response(
                description="Password changed successfully",
                examples={
                }
            )
        }
    ),

    'ForgetPasswordAPISchema' : dict(
        operation_description='Request a forget-link for password reset',
        operation_summary='send password reset link',
        responses={
            "200": openapi.Response(
                description="Forget-link for password reset sent",
                examples={
                }
            )
        }
    ),

    'ResetPasswordAPISchema' : dict(
        operation_description='Reset new password',
        operation_summary='Reset password',
        responses={
            "200": openapi.Response(
                description="Password successfully reset",
                examples={
                }
            )
        }
    ),

    'CustomTokenObtainPairSchema' : dict(
        operation_description='Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials.',
        operation_summary='JWT tokens',
        responses={
            "200": openapi.Response(
                description="Tokens successfully recieved",
                examples={
                    "application/json": {
                        "refresh": "string",
                        "access": "string",
                    }
                }
            )
        }
    ),

    'CustomTokenRefreshViewSchema' : dict(
        operation_description='Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.',
        operation_summary='Get access token',
        responses={
            "200": openapi.Response(
                description="Access Token successfully recieved",
                examples={
                    "application/json": {
                        "access": "string",
                    }
                }
            )
        }
    ),

    'LogoutAPIViewSchema' : dict(
        operation_description='Refresh token needs to be present in request data. Also the user needs to be authenticated or in another way, access token needs to be present in request header. Requesting to this endpoint with these properties will logout the user.',
        operation_summary='Logout the user',
        responses={
            "200": openapi.Response(
                description="Successful Logout"
            ),
            "401": openapi.Response(
                description="Unsuccessful Logout due to unauthorized or unauthenticated request."
            )
        }
    ),

    'UserAPIViewSchema' : dict(
        operation_description='Get information of user in User model',
        operation_summary='User model instance information',
        responses={
            "200": openapi.Response(
                description="User info",
                examples={
                    "application/json": {
                        "id": "integer",
                        "email" : "string",
                        "firstname" : "string",
                        "lastname" : "string"
                    }
                }
            ),
            "401": openapi.Response(
                description="Unsuccessful unauthorized or unauthenticated request."
            )
        }
    ),
}

