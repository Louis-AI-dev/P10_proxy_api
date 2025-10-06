import logging
import azure.functions as func
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Requête reçue sur proxyAPI.')

    # Récupération des paramètres GET
    user_id = req.params.get('user_id')
    method = req.params.get('method', 'collaborative')

    if not user_id:
        return func.HttpResponse(
            "Paramètre user_id manquant",
            status_code=400
        )

    # Requête vers l'API render.com
    api_url = f"https://p10-api-latest.onrender.com/get_recos?user_id={user_id}&method={method}"
    try:
        resp = requests.get(api_url)
        return func.HttpResponse(resp.text, status_code=resp.status_code)
    except Exception as e:
        return func.HttpResponse(f"Erreur lors de l'appel à l'API: {e}", status_code=500)
