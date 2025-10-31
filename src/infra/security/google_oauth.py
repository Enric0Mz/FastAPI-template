import os

from authlib.integrations.starlette_client import OAuth


from src.helpers.load_env import custom_loadenv

custom_loadenv()


ENV = os.getenv("ENVIROMENT", "production")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "fallback_id")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "fallback_secret")


if ENV == "development":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


oauth = OAuth()

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
