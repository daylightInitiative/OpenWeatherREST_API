# Start the backend in a new Command Prompt window
Start-Process powershell -ArgumentList "-NoExit", "-File", "bootstrap.ps1"


# Wait for Flask to start
Start-Sleep -Seconds 5

# Create and send the JSON payload (ISO 3166-1 ALPHA-2 standard)
$body = @{
    city = "Tokyo"
    country = "JP"
}
$json = $body | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/weather-sentiment" `
                  -Method POST `
                  -ContentType "application/json" `
                  -Body $json
