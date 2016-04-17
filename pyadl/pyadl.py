import requests
from pywebhdfs.webhdfs import PyWebHdfsClient


class AuthenticationError(Exception):
    """AuthenticationError is raised when the DataLakeHDFS object cannot obtain a token from AAD"""
    pass


class PyDataLakeClient(object):
    """PyDataLakeClient is a wrapper for PyWebHdfsClient that sets the Authorization header and base_uri_pattern for Azure Data Lake Store"""
    def __init__(self, store_name, client_id, client_secret, tenant_id):
        """
        Create ADL wrapper object with given parameters:

        `store_name`: name of your ADL store (the first part of the URL, e.g. <NAME>.azuredatalakestore.net)
        `client_id`: Client ID of the Azure Active Directory application
        `client_secret`: Valid key for the Azure Active Directory application
        `tenant_id`: Tenant ID of the Azure Active Directory application. You can get this from the "endpoints" modal at the bottom of the AAD application page.

        For more information on any of the parameters see https://github.com/Azure/azure-content/blob/master/articles/data-lake-store/data-lake-store-get-started-rest-api.md.
        """
        oauth2_endpoint = "https://login.microsoftonline.com/{0}/oauth2/token".format(tenant_id)

        self._webhdfs_url = "https://{0}.azuredatalakestore.net/webhdfs/v1/".format(store_name)

        r = requests.post(oauth2_endpoint, data={
            'grant_type': 'client_credentials',
            'resource': 'https://management.core.windows.net',
            'client_id': client_id,
            'client_secret': client_secret})

        if r.status_code != 200:
            raise AuthenticationError("Error authenticating to AAD {0}: {1}".format(r.status_code, r.text))

        self._token = r.json()['access_token']

    def client(self):
        """Return WebHDFS object correctly configured for ADL"""
        return PyWebHdfsClient(base_uri_pattern=self._webhdfs_url, request_extra_opts={
            'headers': {"Authorization": "Bearer {0}".format(self._token)}
        })
