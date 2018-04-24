"""Book-A-Meal Version 1.0 Documentation
"""
CREATE_POST_DOCS = {
    "tags": [
        "Meal"
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
                        "example": "The first meal"
                    },
                    "price": {
                        "type": "float"
                        "example": 200.00
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