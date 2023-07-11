from drf_yasg import openapi


schemas = {

    'BloodTestViewSetSchema' : {
        'CREATE' : dict(
            operation_description="""
            Create a new blood test:

            `1- "gender" : categorical inter (get the possible integers from "/checkup/api/check-up/values/" in GenderType section of the response)`

            `2- "title" : a title for the blood test`

            `3- "description" : description for the blood test (allowed to be blank)`
            """,
            operation_summary="Create a new blood test",
            responses={
                "201": openapi.Response(
                    description="blood test created",
                    examples={
                        'application/json' : {
                            "id": "string",
                            "gender": "categorical integer",
                            "title": "string",
                            "description": "string"
                        }
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'LIST' : dict(
            operation_description='List all of the existing blood tests.',
            operation_summary="List all of the existing blood tests",
            responses={
                "200": openapi.Response(
                    description="All blood tests retrieved",
                    examples={
                        'application/json' : [
                                {
                                "id": "string",
                                "gender": "categorical string",
                                "title": "string",
                                "description": "string"
                            },
                                {
                                "id": "string",
                                "gender": "categorical string",
                                "title": "string",
                                "description": "string"
                            }
                        ]    
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'RETRIEVE' : dict(
            operation_description='Retrieve a blood test with its id.',
            operation_summary="Retrieve a blood test with its id",
            responses={
                "200": openapi.Response(
                    description="Blood test retrieved",
                    examples={
                        'application/json' : {
                                "id": "string",
                                "gender": "categorical string",
                                "title": "string",
                                "description": "string"
                        },
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'UPDATE' : dict(
            operation_description="""
            Update a blood test with its id:
            
            `1- "gender" : categorical inter (get the possible integers from "/checkup/api/check-up/values/" in GenderType section of the response)`

            `2- "title" : a title for the blood test`

            `3- "description" : description for the blood test (allowed to be blank)`
            """,
            operation_summary="Update a blood test with its id",
            responses={
                "200": openapi.Response(
                    description="Blood test updated",
                    examples={
                        'application/json' : {
                                "id": "string",
                                "gender": "categorical string",
                                "title": "string",
                                "description": "string"
                        },
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'DESTROY' : dict(
            operation_description='Delete an existing blood test. The results of this blood test will be deleted as well.',
            operation_summary="Delete an existing blood test",
            responses={
                "204": openapi.Response(
                    description="blood test deleted",
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
    },

    'BloodTestResultsViewSetSchema' : {
        'CREATE' : dict(
            operation_description="""
            Create a new result for an existing blood test :

            `1- "name" : categorical inter (get the possible integers from "/checkup/api/check-up/values/" in BloodTestArticles section of the response)`

            `2- "value" : a decimal number (6 digits in total 3 of which are decimal)`

            `3- "blood_test_id" : id of the existing blood test for which you want to add results `
            """,
            operation_summary="Create a new result for an existing blood test",
            responses={
                "201": openapi.Response(
                    description="blood test created",
                    examples={
                        'application/json' : {
                            "id": "string",
                            "name": "categorical integer",
                            "value": "a decimal number",
                        }
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'RETRIEVE' : dict(
            operation_description='Retrieve a blood test result with its id.',
            operation_summary="Retrieve a blood test with its id",
            responses={
                "200": openapi.Response(
                    description="Blood test result retrieved",
                    examples={
                        'application/json' : {
                                "id": "string",
                                "name": "categorical integer",
                                "value": "a decimal number",
                        },
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'UPDATE' : dict(
            operation_description="""
            Update a blood test result with its id :

            `1- "name" : categorical inter (get the possible integers from "/checkup/api/check-up/values/" in BloodTestArticles section of the response)`

            `2- "value" : a decimal number (6 digits in total 3 of which are decimal)`

            `3- "blood_test_id" : id of the existing blood test for which you want to add results `
            """,
            operation_summary="Update a blood test result with its id",
            responses={
                "200": openapi.Response(
                    description="Blood test result updated",
                    examples={
                        'application/json' : {
                                "id": "string",
                                "name": "categorical integer",
                                "value": "a decimal number",
                        },
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'DESTROY' : dict(
            operation_description='Delete a blood test result with its id.',
            operation_summary="Delete a blood test result with its id",
            responses={
                "204": openapi.Response(
                    description="blood test result deleted",
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
    },

    'CheckUpCategoricalValuesAPISchema' : dict(
        operation_description='Retrieve categorical values of blood test fields.',
        operation_summary="Retrieve categorical values of blood test fields",
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

    'BloodTestDetailsViewSetSchema' : {
        'CREATE' : dict(
            operation_description="""
            Create a new blood test with its results together :

            `1- "blood_test_results" : a list containing dictionaries of the blood test result. Each blood test result can be added to this list as below :`

                    {
                    "name" : categorical inter (get the possible integers from "/checkup/api/check-up/values/" in BloodTestArticles section of the response),
                    "value" : a decimal number (6 digits in total 3 of which are decimal)
                    }

            `2- "gender" : categorical inter (get the possible integers from "/checkup/api/check-up/values/" in GenderType section of the response)`

            `3- "title" : a title for the blood test`

            `4- "description" : description for the blood test (allowed to be blank)`
            """,
            operation_summary="Create a new blood test with its results together",
            responses={
                "201": openapi.Response(
                    description="blood test created",
                    examples={
                        'application/json' : {
                            "id": "string",
                            "blood_test_results": [
                                {
                                "id": "string",
                                "name": "categorical string",
                                "value": "a decimal number"
                                }
                            ],
                            "gender": "categorical string",
                            "title": "string",
                            "description": "string"
                        }
                    }
                ),
                "401": openapi.Response(
                    description="Authentication credentials were not provided",
                ),
            }
        ),
        'RETRIEVE' : dict(
            operation_description='Retrieve a blood test alongside with its related results with blood test id.',
            operation_summary="Retrieve a blood test alongside the results",
            responses={
                "200": openapi.Response(
                    description="Blood test and related result retrieved",
                    examples={
                        'application/json' : {
                            "id": "string",
                            "blood_test_results": [
                                {
                                "id": "string",
                                "name": "categorical string",
                                "value": "a decimal number"
                                }
                            ],
                            "gender": "categorical string",
                            "title": "string",
                            "description": "string"
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

