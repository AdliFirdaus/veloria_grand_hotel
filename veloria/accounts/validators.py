import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class StrongPasswordValidator:
    def validate(self, password, user=None):
        errors = []
        if not re.search(r'[A-Z]', password):
            errors.append(_('Password must contain at least one uppercase letter.'))
        if not re.search(r'[a-z]', password):
            errors.append(_('Password must contain at least one lowercase letter.'))
        if not re.search(r'\d', password):
            errors.append(_('Password must contain at least one digit.'))
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append(_('Password must contain at least one special character.'))
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _(
            'Password must contain uppercase, lowercase, digit, and special character.'
        )
