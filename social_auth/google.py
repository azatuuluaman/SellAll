from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            data_info = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if 'accounts.google.com' in data_info['iss']:
                return data_info

        except:
            return "The token is either invalid or has expired"
