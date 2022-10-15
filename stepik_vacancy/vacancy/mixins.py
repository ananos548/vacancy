from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse
import logging

from .models import Company

logger = logging.getLogger(__name__)


class OnlyUserWithCompanyMixin:

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'company'):
            logger.warning('User without a company tries to do something only for users without a company',
                           request.user.pk, )
            return redirect(reverse('letsstart'))
        return super().dispatch(request, *args, **kwargs)


class OnlyUserWithoutCompanyMixin:

    def dispatch(self, request, *args, **kwargs):
        if Company.objects.filter(
                owner=request.user).exists():  # exists() возвращает True , если возвращаемый QuerySet содержит один или несколько объектов, и значение False , если QuerySet пустой
            logger.warning('User with a company tries to do something only for users with a company',
                           request.user.pk, )
            return redirect(reverse('mycompany'))
        return super().dispatch(request, *args, **kwargs)
