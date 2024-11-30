from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GITLAB_CLIENT_ID: str = "not_set"
    GITLAB_CLIENT_SECRET: str = "not_set"
    GITLAB_REDIRECT_URI: str = "https://review.gitcto.space/api/gitlab/auth/callback"

    GITLAB_AUTH_URL: str = "https://gitlab.com/oauth/authorize"
    GITLAB_TOKEN_URL: str = "https://gitlab.com/oauth/token"
    GITLAB_API_URL: str = "https://gitlab.com/api/v4/user"


settings = Settings()
