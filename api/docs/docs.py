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

GET_MEAL_DOCS = {
    "tags": [
        "Book-A-Meal"
    ],
    "description": "Get meal details",
    "parameters": [
        {
            "name": "meal_id",
            "in": "path",
            "description": "meal id",
            "schema": {
                "type": "string",
                "format": "uuid",
            },
            "required": True,
        }
    ],
    "responses": {
        "200": {
            "description": "Return response status and message and meal details",
            "schema": {
                "id": "get_meal_response",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "ok"
                    },
                    "message": {
                        "type": "string",
                        "example": "meal found"
                    },
                    "meal": {
                        "type": "object",
                        "schema": {
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "example": "a69de3743ae24ac89dc3dc2e54c91b3b"
                                },
                                "title": {
                                    "type": "string",
                                    "example": "The First Post"
                                },
                                "price": {
                                    "type": "float",
                                    "example": "400.00"
                                },
                            }
                        }
                    },
                }
            },
        }
    }
}

UPDATE_MEAL_DOCS = {
    "tags": [
        "Book-A-Meal"
    ],
    "description": "Update meal details by the authenticated caterer",
    "parameters": [
        {
            "name": "meal_id",
            "in": "path",
            "description": "Meal id",
            "type": "string",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "description": "New meal details",
            "required": True,
            "schema": {
                "id": "update_meal_data",
                "required": [
                    "title",
                    "price",
                ],
                "properties": {
                    "title": {
                        "type": "string",
                        "example": "Chicken with fish"
                    },
                    "price": {
                        "type": "float",
                        "example": "3000.00"
                    },
                }
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Return response status and response message",
            "schema": {
                "id": "update_meal_response",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "ok"
                    },
                    "message": {
                        "type": "string",
                        "example": "Meal has been successfully updated"
                    },
                }
            }
        }
    }
}