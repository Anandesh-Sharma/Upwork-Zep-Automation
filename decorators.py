def handle_login_failures(func):
    def wrapper(self):
        try:
            # call the function
            url = func(self)

            if 'CLIENTSESSID' in url:
                print(f'>>> login successful : URL : {url}')
                return True

        except Exception as e:
            print(f'!! Exception occurred at login step : {str(e)}')

        return False

    return wrapper


def handle_timezone_failures(func):
    def wrapper(self):
        try:
            # call the function
            found_token_and_session_id = func(self)

            if found_token_and_session_id:
                print(f'>>> Successfully changed the timezone, acquired request token and client session id')
                print(f'>>> client_id : {self.client_session_id} | request_token : {self.request_token}')
                return True

        except Exception as e:
            print(f'!! Exception occurred at timezone step : {str(e)}')

        return False

    return wrapper


def handle_payload_id_extraction(func):
    def wrapper(self, ticket_id):
        try:
            # call the function
            status, ids = func(self, ticket_id)
            if status:
                print(f'>>> IDs found for zep ticket id = {ticket_id} : occurrence_id = {ids[0]} & project_id = {ids[1]}')
                return ids
            else:
                print(f'!! Unable to extract payload ids for ticket_id : {ticket_id}')
                exit()

        except Exception as e:
            print(f'!! Exception occurred at payload id extraction step : {str(e)}')

        return False

    return wrapper


def handle_post_time_failures(func):
    def wrapper(self, data):
        try:
            # call the function
            response = func(self, data)
            response_json = response.json()

            if response.status_code == 200 and response_json['requesttoken']:
                self.request_token = response_json['requesttoken']
                return True
        except Exception as e:
            print(f'!! Exception occurred at post_time step : {str(e)}')

        return False

    return wrapper
