from drf_yasg import openapi


schemas = {
    'ActivateDeviceAPISchema' : {
        'PATCH' : dict(
            operation_description='Enter recieved code and activate the device.',
            operation_summary="Activate device.",
            responses={
                "200": openapi.Response(
                    description="device activated successfully",
                ),
                "404": openapi.Response(
                    description="No device found!",
                ),
            }
        ),
        'GET' : dict(
            operation_description='Request for activation code resend.',
            operation_summary="Resend activation code",
            responses={
                "201": openapi.Response(
                    description="Activation code sent",
                    examples={
                        'application/json' : {
                            'device_id' : "string",
                            "expiration_time_seconds" : "integer(seconds)"
                        }
                    }
                ),
                "208": openapi.Response(
                    description="Activation code is already sent and valid.",
                ),
                "404": openapi.Response(
                    description="No device found!",
                ),
            }
        ),
    },

    'DeviceAPISchema' : {
        'CREATE' : dict(
            operation_description='Create a new device.',
            operation_summary="Create new device.",
            responses={
                "201": openapi.Response(
                    description="Device created",
                    examples={
                        'application/json' : {
                            'id' : "string",
                            "api_key" : "string",
                            "name" : "string",
                            "description" : "string",
                            "serial_number": "string",
                            "is_active" : "bool",
                            "expiration_time_seconds" : "integer(seconds)"
                        }
                    }
                ),
            }
        ),
        'LIST' : dict(
            operation_description='List all devices of the authenticated user',
            operation_summary="List all devices",
            responses={
                "200": openapi.Response(
                    description="All devices returned",
                    examples={
                        'application/json' : [
                            {
                                'id' : "string",
                                "api_key" : "string",
                                "name" : "string",
                                "description" : "string",
                                "serial_number": "string",
                                "is_active" : "bool"
                            },
                            {
                                'id' : "string",
                                "api_key" : "string",
                                "name" : "string",
                                "description" : "string",
                                "serial_number": "string",
                                "is_active" : "bool"
                            },
                        ]    
                    }
                ),
            }
        ),
        'RETRIEVE' : dict(
            operation_description='List details of one device, given the device id',
            operation_summary="List one device",
            responses={
                "200": openapi.Response(
                    description="Device returned",
                    examples={
                        'application/json' : {
                            'id' : "string",
                            "api_key" : "string",
                            "name" : "string",
                            "description" : "string",
                            "is_active" : "bool"
                        },
                    }
                ),
            }
        ),
        'UPDATE' : dict(
            operation_description='Update name or description of device',
            operation_summary="update device info",
            responses={
                "200": openapi.Response(
                    description="Device update",
                    examples={
                        'application/json' : {
                            'id' : "string",
                            "api_key" : "string",
                            "name" : "string",
                            "description" : "string",
                            "is_active" : "bool"
                        },
                    }
                ),
            }
        ),
    },
    'OverrideAPIKeySchema' : dict(
        operation_description="Enter device name and request to this url to override device api-key.",
        operation_summary="Override api-key of the device",
        responses={
            "200": openapi.Response(
                description="API-Key successfully overrided",
                examples={
                        'application/json' : {
                            "api_key" : "string",
                        },
                    }
            ),
            "400": openapi.Response(
                description="No device found!",
            ),
        }
    ),
    'DeviceLatestRecordAPISchema' : dict(
        operation_description="A logged in user can request to this url to recieve the latest record of one's devices",
        operation_summary="Get latest record of all active devices of a signed in user",
        responses={
            "200": openapi.Response(
                description="Latest records successfully retrieved",
                examples={
                        'application/json' : {
                            "device1:string" : ("device_id:string", "latest_record:list"),
                            "device2:string" : ("device_id:string", "latest_record:list"),
                            "device3:string" : ("device_id:string", "latest_record:list"),
                        },
                    }
            ),
            "401": openapi.Response(
                description="Authentication credentials were not provided.",
            ),
        }
    )
}

