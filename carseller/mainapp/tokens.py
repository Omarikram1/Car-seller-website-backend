from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, email, timestamp):
        return six.text_type(email) + six.text_type(timestamp)

    def check_token(self, email, token):
        if timezone.now() - timezone.now() < timedelta(minutes=5):
            return super().check_token(email, token)
        return False

email_verification_token = EmailVerificationTokenGenerator()