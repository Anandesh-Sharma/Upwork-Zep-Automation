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

### 2. Create `config.py`
* Just copy the `sample_config.py` content.

### 3. Add config
* Update all necessary config in `config.py`
    ```python
    # upwork creds
    CLIENT_ID = '<upwork client id>'
    CLIENT_SECRET = '<upwork client secret>'

    # contract_id
    CONTRACT_ID = '<upwork contract id>'

    # Zep creds should be in urlencoded form
    USERNAME = '<zep username urlencoded>'
    PASSWORD = '<zep password urlencoded>'

    ```
### 4. Execute `run.py`
* By default this code will pick today's date, if you want to log hours for different day then just update here in `run.py`:
    ```python
    api = Upwork()
    data = api.get_work_diary(<custom datetime object here>, CONTRACT_ID)
    for i in data:
        result = client.post_time(i)
        if not result:
            print(f'!! Failed : {i}')
    ```
