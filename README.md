## Requirements
1. Python 3.9
2. Ubidots account (optional)

## Configuration

1. Create python's virtual environment:  
```bash 
python -m venv venv
```

2. Activate created environment:
 * Powershell (Windows):
    ```bash 
    ./venv/Scripts/Activate.ps1
    ```

 * Linux or git bash:
   ```bash
   source venv/Scripts/activate
   ```

3. Install modules:
```bash
pip install .
```

4. Add Ubidots account's token and API's URL to .env file or as an environmental variable (optional):
```bash
URL=YOUR_DEVICE_URL
TOKEN=YOUR_TOKEN
```

5. Run the application:
```bash
python -m aipo
```