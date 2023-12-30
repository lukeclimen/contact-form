import azure.functions as func
import logging
from Email import _send_email, _create_acknowledgement_email, _create_internal_email

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="contact_form")
async def contact_form(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
        name = req_body.get('name')
        email = req_body.get('email')
        message = req_body.get('message')
    except ValueError:
        return func.HttpResponse(
            "Missing one or more paramters.",
            status_code=400
        )
    try:
        internal_email_copy = _create_internal_email(name, email, message)
        # external_email_copy = _create_acknowledgement_email(name, email, message)
        await _send_email(internal_email_copy)
        # _send_email(external_email_copy)
        return func.HttpResponse(
            "Successfully submitted contact form.",
            status_code=200
        )
    except Exception as ex:
        print(ex)
        return func.HttpResponse(
            "Error while submitting form.",
            status_code=500
        )
