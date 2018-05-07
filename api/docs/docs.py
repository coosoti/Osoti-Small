"""Book-A-Meal Version 1.0 Documentation"""
CREATE_MEAL_DOCS = {
    "tags": [
        "Meal"
    ],
    "description": "Meal Creation",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "bytes",
            },
            "required": True,
        },
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
        "Meal"
    ],
    "description": "Get a list of meals created by authenticated caterer",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "bytes",
            },
            "required": True,
        }
    ],
    "responses": {
        "200": {
            "description": "Return response status and message and a list of meals by the caterer",
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
                                    "example": "int"
                                },
                                "title": {
                                    "type": "string",
                                    "example": "Beef with chicken"
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
        "Meal"
    ],
    "description": "Get meal details",
    "parameters": [
        {
            "name": "meal_id",
            "in": "path",
            "description": "meal id",
            "schema": {
                "type": "int",
                "format": "int",
            },
            "required": True,
        },
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "bytes",
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
                                    "example": "int"
                                },
                                "title": {
                                    "type": "string",
                                    "example": "Samaki"
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
        "Meal"
    ],
    "description": "Update meal details by the authenticated caterer",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "bytes",
            },
            "required": True,
        },
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

DELETE_MEAL_DOCS = {
    "tags": [
        "Meal"
    ],
    "description": "Meal can only be deleted by authenticated caterer",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "int",
            },
            "required": True,
        },
        {
            "name": "meal_id",
            "in": "path",
            "description": "meal id",
            "type": "string",
            "required": True,
        },
    ],
    "responses": {
        "202": {
            "description": "Return response status and response message",
            "schema": {
                "id": "delete_meal_response",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "ok"
                    },
                    "message": {
                        "type": "string",
                        "example": "Meal option has been successfully deleted"
                    },
                }
            }
        }
    }
}

SIGNUP_DOCS = {
    "tags": [
        "User"
    ],
    "description": "User registration",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "description": "User details",
            "required": True,
            "schema": {
                "id": "User",
                "required": [
                    "username",
                    "email",
                    "designation"
                    "password",
                    "confirm_password",
                ],
                "properties": {
                    "username": {
                        "type": "string",
                        "minimum": 6,
                        "example": "osoticharles",
                    },
                    "email": {
                        "type": "email",
                        "example": "osoticharles@gmail.com"
                    },
                    "designation": {
                        "type": "string",
                        "example": "caterer"
                    },
                    "password": {
                        "type": "string",
                        "example": "kulundeng",
                    },
                    "confirm_password": {
                        "type": "string",
                        "example": "kulundeng",
                    },
                }
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Return response status and message",
            "schema": {
                "id": "registration_response",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "ok"
                    },
                    "message": {
                        "type": "string",
                        "example": "You have been successfully registered"
                    },
                    "auth_token": {
                        "type": "string",
                        "example": "auth_token....."
                    },
                }
            }
        }
    }
}

SIGNIN_DOCS = {
    "tags": [
        "User"
    ],
    "description": "User login by providing valid credentials",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "description": "User credentials",
            "required": True,
            "schema": {
                "id": "login",
                "required": [
                    "email",
                    "password"
                ],
                "properties": {
                    "email": {
                        "type": "email",
                        "example": "osoticharles@gmail.com"
                    },
                    "password": {
                        "type": "string",
                        "example": "kulundeng"
                    },
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Return response status and message",
            "schema": {
                "id": "login_response",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "ok"
                    },
                    "message": {
                        "type": "string",
                        "example": "You have been successfully logged in"
                    },
                    "auth_token": {
                        "type": "string",
                        "example": "auth_token....."
                    },
                }
            }
        }
    }
}

SIGNOUT_DOCS = {
    "tags": [
        "User"
    ],
    "description": "User logout",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "bytes",
            },
            "required": True,
        }
    ],
    "responses": {
        "200": {
            "description": "Return response status and message",
            "schema": {
                "id": "logout_response",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "ok"
                    },
                    "message": {
                        "type": "string",
                        "example": "You have successfully logged out"
                    },
                }
            }
        }
    }
}


CREATE_MENU_DOCS = {
    "tags": [
        "Menu"
    ],
    "description": "Menu Creation",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "bytes",
            },
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "description": "meal id",
            "required": True,
            "schema": {
                "id": "menu_set",
                "required": [
                    "selected_ids"
                ],
                "properties": {
                    "selected_id": {
                        "type": "int",
                        "example": ["1"]
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
                        "example": "Menu for today has been successfully created"
                    },
                }
            }
        }
    }
}

GET_MENU_DOCS = {
    "tags": [
        "Menu"
    ],
    "description": "Get a list of menu created by authenticated caterer",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "bytes",
            },
            "required": True,
        }
    ],
    "responses": {
        "200": {
            "description": "Return response status and message and a list of meals in the menu",
            "schema": {
                "id": "get_meals_response",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "ok"
                    },
                    "message": {
                        "type": "string",
                        "example": "You have 1 menu"
                    },
                    "date": {
                        "type": "date",
                        "example": "2018-11-25"
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
                                    "example": "Beef with chicken"
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

MAKE_ORDER_DOCS = {
    "tags": [
        "Order"
    ],
    "description": "Get a list of menu created by authenticated caterer",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "bytes",
            },
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "description": "meal id",
            "required": True,
            "schema": {
                "id": "menu_set",
                "required": [
                    "selected_meal_id"
                ],
                "properties": {
                    "id": {
                        "type": "int",
                        "example": "1"
                    },
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Return response status and message on the success of the order user",
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
                    "orders ": {
                        "type": "array",
                        "items": {
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "example": "1"
                                },
                                "title": {
                                    "type": "string",
                                    "example": "Beef with chicken"
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

UPDATE_ORDER_DOCS = {
    "tags": [
        "Order"
    ],
    "description": "Update order details by the authenticated customer",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "bytes",
            },
            "required": True,
        },
        {
            "name": "order_id",
            "in": "path",
            "description": "order id",
            "type": "string",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "description": "New order details",
            "required": True,
            "schema": {
                "id": "update_order_data",
                "required": [
                    "selected_meal_id",
                ],
                "properties": {
                    "selected_meal_id": {
                        "type": "int",
                        "example": "1"
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

GET_ORDERS_DOCS = {
    "tags": [
        "Order"
    ],
    "description": "Get a list of orders made by authenticated customers",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "bytes",
            },
            "required": True,
        }
    ],
    "responses": {
        "200": {
            "description": "Return response status and message and a list of orders",
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
                                    "example": "1"
                                },
                                "title": {
                                    "type": "string",
                                    "example": "Beef with chicken"
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

GET_ORDER_DOCS = {
    "tags": [
        "Order"
    ],
    "description": "Get order made by authenticated customers",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "description": "Authorization token",
            "schema": {
                "type": "string",
                "format": "bytes",
            },
            "required": True,
        },
        {
            "name": "order_id",
            "in": "path",
            "description": "order id",
            "type": "string",
            "required": True,
        }
    ],
    "responses": {
        "200": {
            "description": "Return response status and message and a list of orders by the user",
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
                                    "type": "int",
                                    "example": "1"
                                },
                                "title": {
                                    "type": "string",
                                    "example": "Beef with chicken"
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
