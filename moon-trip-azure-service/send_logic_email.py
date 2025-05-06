import logging
import requests

def main():

    logic_app_url = 'https://prod-10.northcentralus.logic.azure.com:443/workflows/24da40b254f1492ab4664c5932f3d224/triggers/When_a_HTTP_request_is_received/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=LvgDQBfH2PdYIK-SnBhZumuHiu2WIggjBUUlJwpYzT4'

    payload = {
        "email": "tvandy600@gmail.com",
        "subject": "Test Email from Azure Function",
        "message": "This email was triggered by a local script calling a Logic App."
    }

    try:
        response = requests.post(logic_app_url, json=payload)
        if response.status_code in (200, 202):
            print("Logic App triggered successfully.")
        else:
            print(f"Failed: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(str(e))
        print("Error calling Logic App.")

if __name__ == "__main__":
    main()
