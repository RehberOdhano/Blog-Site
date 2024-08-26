from enum import Enum


class ResponseMessages(Enum):
    USER_WITH_SAME_EMAIL_ALREADY_EXISTS = "User with the same email '{{email}}' already exists!"
    USER_NOT_FOUND = "User with id {{id}} is not found!"
    BLOG_WITH_SAME_TITLE_ALREADY_EXISTS = "Blog with the same title '{{title}}' already exists!"
    BLOGS_NOT_FOUND_FOR_THIS_USER = "No blogs found for this user!"
