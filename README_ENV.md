# Environment variables and secrets

This project reads configuration and secrets from environment variables (via python-dotenv when running locally). Never hardcode secrets in source.

Required variables (set in `.env` or in your environment):

- SECRET_KEY: Django secret key. Generate with Django's `get_random_secret_key()` for production.
- DEBUG: true/false (development use true, set to false in production).
- ALLOWED_HOSTS: comma-separated list of allowed hosts (used when DEBUG is false).
- CORS_ALLOWED_ORIGINS: comma-separated list of allowed CORS origins (include scheme), e.g. `https://app.example.com,http://localhost:3000`.
- API_KEY: API key used to authenticate requests to `/api/*` endpoints. Keep secret.

Example: copy `.env.example` to `.env` and edit values.

Security notes:

- Keep your `.env` out of version control. `.gitignore` contains `.env` by default.
- Rotate `API_KEY` periodically and use secure storage for production secrets.
- Ensure `DEBUG=False` and a strong `SECRET_KEY` in production.
