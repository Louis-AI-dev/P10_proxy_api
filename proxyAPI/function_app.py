import logging
import azure.functions as func
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="proxyAPI")
def proxyAPI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Requête reçue par la fonction proxyAPI.')

    user_id = req.params.get('user_id')
    method = req.params.get('method')

    if not user_id or not method:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        user_id = user_id or req_body.get('user_id')
        method = method or req_body.get('method')

    if not user_id or not method:
        return func.HttpResponse(
            "Paramètres manquants : user_id et method sont requis.",
            status_code=400
        )

    api_url = f"https://p10-api-latest.onrender.com/get_recos?user_id={user_id}&method={method}"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        return func.HttpResponse(response.text, mimetype="application/json")
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la requête API : {e}")
        return func.HttpResponse(
            f"Erreur de connexion à l'API : {str(e)}",
            status_code=500
        )
