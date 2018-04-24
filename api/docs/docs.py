"""Book-A-Meal Version 1.0 Documentation
"""
CREATE_MEAL_DOCS = {
    "tags": [
        "Book-A-Meal"
    ],
    "description": "Meal Creation",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "description": "New meal details",
            "required": True,
            "schema": {
                "id": "new_meal_details",
                "required": [
                    "title",
                    "price",
                ],
                "properties": {
                    "title": {
                        "type": "string",
                        "minimum": 3,
                        "example": "Beef with chicken"
                    },
                    "price": {
                        "type": "float",
                        "example": "200.00"
                    },
                }
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Return response status and response message",
            "schema": {
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "ok"
                    },
                    "message": {
                        "type": "string",
                        "example": "Meal has been successfully created"
                    },
                }
            }
        }
    }
}

GET_MEALS_DOCS = {
    "tags": [
        "Book-A-Meal"
    ],
    "description": "Get a list of meals created by authenticated caterer",
    "responses": {
        "200": {
            "description": "Return response status and message and a list of posts by the user",
            "schema": {
                "id": "get_meals_response",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "ok"
                    },
                    "message": {
                        "type": "string",
                        "example": "You have 1 meal"
                    },
                    "meals": {
                        "type": "array",
                        "items": {
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "example": "a69de3743ae24ac89dc3dc2e54c91b3b"
                                },
                                "title": {
                                    "type": "string",
                                    "example": "PBeef with chicken"
                                },
                                "price": {
                                    "type": "float",
                                    "example": "600.00"
                                },
                            }
                        }
                    },
                }
            },
        }
    }
}