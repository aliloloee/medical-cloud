from drf_yasg import openapi


schemas = {
    'ProfileAPISchema' : dict(
        operation_description='Retrieve Profile information and User information',
        operation_summary="User's full info",
        responses={
            "200": openapi.Response(
                description="Information successfully retrieved",
                examples={
                    "application/json": {
                        "id": "string",
                        "type": "integer",
                        "charge": "string",
                        "user": {
                            "id": "integer",
                            "email": "string",
                            "firstname": "string",
                            "lastname": "string",
                        }
                    }
                }
            ),
            "401": openapi.Response(
                description="Unauthorized or unauthenticated request.",
            ),
        }
    ),

    'ProfileChargeAPISchema' : dict(
        operation_description='Increase profile charge with patch request',
        operation_summary="Increase profile charge",
        responses={
            "200": openapi.Response(
                description="Profile successfully charged",
                examples={
                    "application/json": {
                        "id": "string",
                        "type": "integer",
                        "charge": "string",
                        "user": {
                            "id": "integer",
                            "email": "string",
                            "firstname": "string",
                            "lastname": "string",
                        }
                    }
                }
            ),
            "401": openapi.Response(
                description="Unauthorized or unauthenticated request.",
            ),
        }
    ),

    'CustomProfileAPISchema' : dict(
        operation_description='Retrieve Custom Profile information and User information. Most of the fields here are categorical, in order to recieve these categorical values refer to the related API in "profiles" section.',
        operation_summary="User's custom profile full info",
        responses={
            "200": openapi.Response(
                description="Information successfully retrieved",
                examples={
                    "application/json": {
                        "id": "integer",
                        "user": {
                            "id": "integer",
                            "email": "string",
                            "firstname": "string",
                            "lastname": "string",
                        },
                        "age": "integer",
                        "gender": "categorical-string",
                        "education": "categorical-string",
                        "employment": "categorical-string",
                        "tobacco": "categorical-string",
                        "alcohol": "categorical-string",
                        "physical_activity": "categorical-string",
                        "fruit_consumption": "categorical-string",
                        "vegetable_consumption": "categorical-string",
                        "meat_consumption": "categorical-string",
                        "obesity": "categorical-string",
                        "sedentary_job": "categorical-string",
                        "diabetes_history": "categorical-string",
                        "cholesterol_history": "categorical-string",
                        "blood_pressure_history_on_mother_side": "categorical-string",
                        "blood_pressure_history_on_father_side": "categorical-string",
                        "salty_diet": "categorical-string"
                    }
                }
            ),
            "401": openapi.Response(
                description="Unauthorized or unauthenticated request.",
            ),
        }
    ),

    'CustomProfileCategoricalValuesAPISchema' : dict(
        operation_description='Retrieve categorical values of custom profile fields.',
        operation_summary="Categorical values of custom profile fields",
        responses={
            "200": openapi.Response(
                description="Information successfully retrieved",
                examples={
                    "application/json": {
                        "field1" : {
                            "value1" : "category",
                            "value2" : "category",
                            "value3" : "category",
                        },
                        "field2" : {
                            "value1" : "category",
                            "value2" : "category",
                            "value3" : "category",
                        },
                        "field3" : {
                            "value1" : "category",
                            "value2" : "category",
                            "value3" : "category",
                        }
                    }
                }
            ),
        }
    ),

    'CustomProfileUpdateAPISchema' : dict(
        operation_description='Update Custom profile values. The fields here are mostly categorical, in order to recieve these categorical values refer to the related API in "profiles" section.',
        operation_summary="Update Custom profile values",
        responses={
            "200": openapi.Response(
                description="Information successfully retrieved",
                examples={
                    "application/json": {
                        "age": "positive integer",
                        "gender": "categorical integer",
                        "education": "categorical integer",
                        "employment": "categorical integer",
                        "tobacco": "categorical integer",
                        "alcohol": "categorical integer",
                        "physical_activity": "categorical integer",
                        "fruit_consumption": "categorical integer",
                        "vegetable_consumption": "categorical integer",
                        "meat_consumption": "categorical integer",
                        "obesity": "categorical integer",
                        "sedentary_job": "categorical integer",
                        "diabetes_history": "categorical integer",
                        "cholesterol_history": "categorical integer",
                        "blood_pressure_history_on_mother_side": "categorical integer",
                        "blood_pressure_history_on_father_side": "categorical integer",
                        "salty_diet": "categorical integer"
                    }
                }
            ),
        }
    ),
}

