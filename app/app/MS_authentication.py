from msal import ConfidentialClientApplication, PublicClientApplication, SerializableTokenCache
import os
import uuid


client_secret = os.environ["client_secret"]
client_id = os.environ["client_id"]
tenant_id = os.environ["tenant_id"]
scope = ["User.Read"]
authority = f"https://login.microsoftonline.com/{tenant_id}"
redirect_url = os.environ["redirect_url"]

# The following functions are used to authenticate the user with Microsoft Azure
def build_msal_app(cache=None):
    return ConfidentialClientApplication(client_id, authority=authority,
                                         client_credential=client_secret, token_cache=cache)

# The following function is used to build the authentication URL
def build_auth_url(scopes=scope):
    return build_msal_app().get_authorization_request_url(scopes,
                                state=str(uuid.uuid4()),
                                redirect_uri=redirect_url)

# The following function is used to load the cache
def load_cache(session):
    cache = SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

# The following function is used to save the cache
def save_cache(cache,session):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()
