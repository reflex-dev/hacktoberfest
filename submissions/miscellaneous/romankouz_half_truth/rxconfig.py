import os
import reflex as rx

# Determine if the app is running on Heroku
is_heroku = False

# Set ports based on environment
if is_heroku:
    port = int(os.environ.get("PORT", 8000))  # 8000 as a fallback, though it should always be set by Heroku
else:
    port = 3000  # local frontend port
    backend_port = 8000  # local backend port

# Set URLs based on environment
if is_heroku:
    api_url = f"https://halftruth-902bd155f5ba.herokuapp.com"
    deploy_url = f"https://halftruth-902bd155f5ba.herokuapp.com"
else:
    api_url = f"http://localhost:{backend_port}"
    deploy_url = f"http://localhost:{port}"

print(api_url, deploy_url)

config = rx.Config(
    app_name="half_truth_game",
    loglevel=rx.constants.LogLevel.INFO,
    api_url=api_url,
    deploy_url=deploy_url,
)
