from django.core.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token

def token_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        if auth_token:
            # Split 'Token <token_value>' to get the token value.
            token = auth_token.split(' ')[1]
            try:
                # Check if the token exists.
                Token.objects.get(key=token)
            except Token.DoesNotExist:
                raise PermissionDenied("Invalid token")
        else:
            raise PermissionDenied("Token not provided")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
