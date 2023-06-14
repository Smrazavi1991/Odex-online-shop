from drf_spectacular.extensions import OpenApiAuthenticationExtension
from user.authentication import JWTAuthentication


class JWTAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = JWTAuthentication
    name = 'jwtAuth'
    match_subclasses = True
    override_provides = ['authentication']
    priority = -1

    def get_security_definition(self, auto_schema, **kwargs):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'jwt',
        }
