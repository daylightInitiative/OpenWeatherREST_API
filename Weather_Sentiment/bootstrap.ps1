# Set the environment variable
$env:FLASK_APP = "./WeatherSentiment/main.py"

# Print a message
Write-Host "Running Flask App bootstrap"

# Run Flask with pipenv
pipenv run flask --debug run -h 0.0.0.0