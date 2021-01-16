"""Ecommerce extensions custom backends"""
from auth_backends.backends import PROFILE_CLAIMS_TO_DETAILS_KEY_MAP, EdXOAuth2
from django.conf import settings


class EcommerceExtensionsAuth2(EdXOAuth2):
    """This class is a wrapper of auth_backends.backends.EdXOAuth2, this allows
    to override the value of CLAIMS_TO_DETAILS_KEY_MAP by using django-conf.settings
    """

    @property
    def CLAIMS_TO_DETAILS_KEY_MAP(self):
        return getattr(settings, "PROFILE_CLAIMS_TO_DETAILS_KEY_MAP", PROFILE_CLAIMS_TO_DETAILS_KEY_MAP)
