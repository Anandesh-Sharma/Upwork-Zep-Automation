# Upwork-Zep-Automation
Created to reduce redundant efforts on logging time in zep. **Now we just need to care about memo in the upwork time tracker**. Update below format in UTT and keep it updated with **zep ticket** and the **task** you are doing.

*Format on Upwork Time Tracker*
```json
    {"memo": "working on xyz", "zep_id":1234}
```


## TODO
1. Replace print statements with rotating loggers
2. Add a monitor to watch, pereferrably I would use a telegram bot that keeps me posted incase something doesn't work.
3. For fun, I want to create an alexa skill which will trigger the script on a voice command.

## How to utilize this project?

### 1. Setup upwork

* Get upwork api from here: https://www.upwork.com/services/api/apply
* Get workdiary scope in your api and you will receive client_id and client_secret

### 2. Generate upwork token
* For the first run you need to get the Token, which needs to be done manually. In order to do this just comment the token from config, it will automatically redirect you the authorization page. 

    ```python
        config = upwork.Config({
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "redirect_uri": 'https://localhost', # change it if you've different callback url
                    # 'token': TOKEN
                })
    ```
* Follow the instructions on the terminal, you will get a dictionary of token. Just paste that inside your `config.py` file.
    ```python 
        TOKEN = <token dictionary> # should be in a single line
    ```
* Now uncomment the Token in `workdiary.py` config.

### 3. Add config
* Update all necessary config in `config.py`
    ```python
        CLIENT_ID = ''
        CLIENT_SECRET = ''
        
        # token must be in single line
        TOKEN = None
        
        # contract_id
        CONTRACT_ID = ''
        
        # Zep creds should be in urlencoded form
        USERNAME = ''
        PASSWORD = ''
    ```
### 4. Execute `run.py`
* By default this code will pick today's date, if you want to log hours for different day then just update here:
    ```python
        api = Upwork()
        data = api.get_work_diary(<custom datetime object here>, CONTRACT_ID)
        for i in data:
            result = client.post_time(i)
            if not result:
                print(f'!! Failed : {i}')
    ```
    


