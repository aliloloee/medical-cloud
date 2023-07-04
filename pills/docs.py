from drf_yasg import openapi


schemas = {

    'UniversalPillModelViewSetSchema' : {
        'CREATE' : dict(
            operation_description='Create a new pill. Only staff have permission to this API.',
            operation_summary="Create new pill",
            responses={
                "201": openapi.Response(
                    description="pill created",
                    examples={
                        'application/json' : {
                            "name" : "string",
                            "description" : "string",
                            "application": "string",
                            "is_active" : "bool",
                        }
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'LIST' : dict(
            operation_description='List all the pills for the user. If user is not staff only name, description and application of active pill are responded. For staff users there are no limits and all properties of all pill are included in the response.',
            operation_summary="List all the pills",
            responses={
                "200": openapi.Response(
                    description="All pills returned",
                    examples={
                        'application/json' : [
                            {
                                '(user)' : "(not staff)",
                                "name" : "string",
                                "description" : "string",
                                "application": "string",
                            },
                            {
                                '(user)' : "(staff)",
                                "id": "string",
                                "name": "string",
                                "description": "string",
                                "application": "string",
                                "is_active": "bool",
                                "created": "datetime string",
                                "updated": "datetime string"
                            },
                        ]    
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'RETRIEVE' : dict(
            operation_description='Retrieve a pill with its id. Only staff have permission to this API.',
            operation_summary="Retrieve a pill with its id",
            responses={
                "200": openapi.Response(
                    description="Pill retrieved",
                    examples={
                        'application/json' : {
                            "id": "string",
                            "name": "string",
                            "description": "string",
                            "application": "string",
                            "is_active": "bool",
                            "created": "datetime string",
                            "updated": "datetime string"
                        },
                    }
                ),
                "403": openapi.Response(
                    description="Permission denied",
                ),
            }
        ),
        'UPDATE' : dict(
            operation_description='Update pill. Only staff have permission to this API.',
            operation_summary="update pill",
            responses={
                "200": openapi.Response(
                    description="Pill updated",
                    examples={
                        'application/json' : {
                            "name" : "string",
                            "description" : "string",
                            "application" : "string",
                            "is_active" : "bool"
                        },
                    }
                ),
                "403": openapi.Response(
                    description="Permission denied",
                ),
            }
        ),
        'DESTROY' : dict(
            operation_description='Destroy pill with its id. Only staff have permission to this API.',
            operation_summary="Destroy pill",
            responses={
                "204": openapi.Response(
                    description="Pill deleted",
                ),
                "403": openapi.Response(
                    description="Permission denied",
                ),
            }
        ),
    },
    'UniversalPillLookUpSchema' : dict(
        operation_description="Retrieve names of pill based on thier first letters which is recieved through an argument 'keyword'. This is for the purpose of searching the names of already saved pills in the database.",
        operation_summary="Search for the names of the pills",
        responses={
            "200": openapi.Response(
                description="API-Key successfully overrided",
                examples={
                        'application/json' : [
                            {
                                "name":"pill1"
                            },
                            {
                                "name":"pill2"
                            },
                            {
                                "name":"pill3"
                            },
                        ],
                    }
            ),
            "401": openapi.Response(
                description="Unauthorized request!",
            ),
        }
    ),
    'PillModelViewSetSchema' : {
        'CREATE' : dict(
            operation_description='Create a new pill.',
            operation_summary="Create new pill",
            responses={
                "201": openapi.Response(
                    description="pill created",
                    examples={
                        'application/json' : {
                            "id" : "string",
                            "name" : "string",
                            "description" : "string",
                        }
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'LIST' : dict(
            operation_description='List all the pills for the user.',
            operation_summary="List all the pills",
            responses={
                "200": openapi.Response(
                    description="All pills returned",
                    examples={
                        'application/json' : [
                            {
                                "id" : "string",
                                "name" : "string",
                                "description" : "string",
                            },
                            {
                                "id" : "string",
                                "name" : "string",
                                "description" : "string",
                            },
                            {
                                "id" : "string",
                                "name" : "string",
                                "description" : "string",
                            },
                        ]    
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'RETRIEVE' : dict(
            operation_description='Retrieve a pill with its id.',
            operation_summary="Retrieve a pill with its id",
            responses={
                "200": openapi.Response(
                    description="Pill retrieved",
                    examples={
                        'application/json' : {
                            "id": "string",
                            "name": "string",
                            "description": "string",
                        },
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'UPDATE' : dict(
            operation_description='Update pill.',
            operation_summary="update pill",
            responses={
                "200": openapi.Response(
                    description="Pill updated",
                    examples={
                        'application/json' : {
                            "id" : "string",
                            "name" : "string",
                            "description" : "string",
                        },
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
    },

    'PillAlarmViewSetSchema' : {
        'CREATE' : dict(
            operation_description='Create a new alarm. User needs to send related pill ID alongside the description of its alarm.',
            operation_summary="Create new alarm",
            responses={
                "201": openapi.Response(
                    description="alarm created",
                    examples={
                        'application/json' : {
                            "id": "string",
                            "description": "string",
                            "is_active": "bool",
                        }
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'LIST' : dict(
            operation_description='List all the alarms of the authenticated user',
            operation_summary="List all the alarms",
            responses={
                "200": openapi.Response(
                    description="All alarms listed",
                    examples={
                        'application/json' : [
                            {
                                "id" : "string",
                                "description" : "string",
                                "is_active": "bool",
                            },
                            {
                                "id" : "string",
                                "description" : "string",
                                "is_active": "bool",
                            },
                            {
                                "id" : "string",
                                "description" : "string",
                                "is_active": "bool",
                            },
                        ]    
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'RETRIEVE' : dict(
            operation_description='Retrieve an alarm with its id.',
            operation_summary="Retrieve an alarm with its id",
            responses={
                "200": openapi.Response(
                    description="Alarm retrieved",
                    examples={
                        'application/json' : {
                            "id": "string",
                            "description": "string",
                            "is_active": "bool",
                        },
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'UPDATE' : dict(
            operation_description='Update alarm description.',
            operation_summary="update alarm description",
            responses={
                "200": openapi.Response(
                    description="Alarm updated",
                    examples={
                        'application/json' : {
                            "id" : "string",
                            "description" : "string",
                            "is_active": "bool",
                        },
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
    },

    'AlarmNotificationViewSetSchema' : {
        'CREATE' : dict(
            operation_description='Create a new alarm notification. User needs to send related alarm ID alongside the consumption status off the related pill.',
            operation_summary="Create a new alarm notification",
            responses={
                "201": openapi.Response(
                    description="alarm notification created",
                    examples={
                        'application/json' : {
                            "id": "string",
                            "consumed": "bool",
                            "consumed_at": "datetime string",
                        }
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'LIST' : dict(
            operation_description='List all the alarm notifications of the authenticated user',
            operation_summary="List all the alarm notifications",
            responses={
                "200": openapi.Response(
                    description="All alarm notifications listed",
                    examples={
                        'application/json' : [
                            {
                                "id": "string",
                                "consumed": "bool",
                                "consumed_at": "datetime string",
                            },
                            {
                                "id": "string",
                                "consumed": "bool",
                                "consumed_at": "datetime string",
                            },
                            {
                                "id": "string",
                                "consumed": "bool",
                                "consumed_at": "datetime string",
                            },
                        ]    
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'RETRIEVE' : dict(
            operation_description='Retrieve an alarm notification with its id.',
            operation_summary="Retrieve an alarm notification with its id",
            responses={
                "200": openapi.Response(
                    description="Alarm notification retrieved",
                    examples={
                        'application/json' : {
                            "id": "string",
                            "consumed": "bool",
                            "consumed_at": "datetime string",
                        },
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'PARTIAl_UPDATE' : dict(
            operation_description='Partial update of an alarm notification with its id.',
            operation_summary="Partial update of an alarm notification with its id.",
            responses={
                "200": openapi.Response(
                    description="Alarm notification update",
                    examples={
                        'application/json' : {
                            "id": "string",
                            "consumed": "bool",
                            "consumed_at": "datetime string",
                        },
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
    },
}

