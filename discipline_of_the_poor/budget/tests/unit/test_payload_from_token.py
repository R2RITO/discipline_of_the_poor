"""
Module used to test the utils/token_utils/payload_from_token method,
used to retrieve the user data from the JWT token
"""
from budget.utils.token_utils import payload_from_token
from django.test import TestCase


class PayloadFromTokenTest(TestCase):

    def test_payload_from_token(self):
        token = """
            eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNz
            IiwiZXhwIjoxNjA0NTQ1MjYzLCJqdGkiOiI2NzRhYzY3OGZkMWY0ZDUyYjRmMDU2M
            mRiOGJjNTVmMyIsInVzZXJfaWQiOjR9.yOASV2YeUgWVxLy5PzPi7XXHP-dhoXeO9
            P4ReKdXEOE
        """

        token_data = payload_from_token(token)

        assert token_data.get('user_id') == 4
