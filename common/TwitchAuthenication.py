from django.db import close_old_connections
from django.contrib.auth.models import User
class TwitchAuthenication:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        # Look up user from query string (you should also do things like
        # check it's a valid user ID, or if scope["user"] is already populated)
        user = User.objects.get(id=int(scope["query_string"]))
        close_old_connections()
        print("hello im here")
        # Return the inner application directly and let it run everything else
        return self.inner(dict(scope, user=user))