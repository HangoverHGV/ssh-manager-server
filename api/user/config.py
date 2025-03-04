"""
This file contains the configuration for the user response examples in Swagger UI.
"""

from os import getenv

USER_GET_ALL_RESPONSE_CONFIG = {
    200: {
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 1,
                        "name": "John Doe",
                        "email": "johndoe@email.com"
                    },
                    {
                        "id": 2,
                        "name": "Jane Doe",
                        "email": "janedoe@email.com"
                    }
                ]
            },
        },
        "description": "Users fetched successfully"
    },
}

USER_GET_RESPONSE_CONFIG = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john_doe@email.com"
                }
            },
        },
        "description": "User fetched successfully"
    }
}

USER_POST_RESPONSE_CONFIG = {
    201: {
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john_doe@email.com"
                }
            },
        },
        "description": "User created successfully"
    },
    400: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "Email already registered"
                }
            },
        },
        "description": "Email already registered"
    }
}

USER_DELETE_RESPONSE_CONFIG = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "User deleted successfully"
                }
            },
        },
        "description": "User deleted successfully"
    },
    404: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not found"
                }
            },
        },
        "description": "User not found"
    },
    401: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "You don't have permission to delete this user"
                }
            },
        },
        "description": "You don't have permission to delete this user"
    }
}

USER_EDIT_RESPONSE_CONFIG = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "johndoe@email.com",
                    "is_active": True,
                    "is_superuser": False
                }
            },
        },
        "description": "User edited successfully"
    },
    404: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not found"
                }
            },
        },
        "description": "User not found"
    },
    401: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "You don't have permission to edit this user"
                }
            },
        },
        "description": "You don't have permission to edit this user"
    }
}

USER_ME_RESPONSE_CONFIG = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "johndoe@email.com",
                }
            },
        },
        "description": "User fetched successfully"
    },
    401: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid credentials"
                }
            },
        },
        "description": "Invalid credentials"
    },
    404: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not found"
                }
            },
        },
        "description": "User not found"
    }
}

USER_MY_USER_RESPONSE_CONFIG = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "johndoe@example.com"
                }
            },
        },
        "description": "User fetched successfully"
    },
    401: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid credentials"
                }
            },
        },
        "description": "Invalid credentials"
    },
    404: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not found"
                }
            },
        },
        "description": "User not found"

    }
}

TOKEN_RESPONSE = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    "access_token": "<TOKEN>",
                    "token_type": "bearer"
                }
            },
        },
        "description": "Token fetched successfully"
    },
    401: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "Incorrect email or password"
                }
            },
        },
        "description": "Invalid credentials"
    }
}

SUPERUSER_SECRET_TOKEN = getenv("SUPERUSER_SECRET_TOKEN")