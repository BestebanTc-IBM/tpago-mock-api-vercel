import json
import re
from flask import Flask, request, Response

app = Flask(__name__)


def parse_body():
    """Lee el body crudo y parsea JSON sin importar Content-Type."""
    try:
        raw = request.get_data(as_text=True).strip()
    except Exception:
        return {}
    if not raw:
        return {}
    # Quitar prefijo "json" que Postman agrega en modo Text
    raw = re.sub(r"^json\s*", "", raw, flags=re.IGNORECASE).strip()
    # Quitar trailing commas
    raw = re.sub(r",\s*([\}\]])", r"\1", raw)
    try:
        return json.loads(raw)
    except Exception:
        return {}


def ok(data):
    return Response(json.dumps(data), status=200, mimetype="application/json")


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.post("/consultar-cuenta-principal")
def consultar_cuenta_principal():
    body = parse_body()
    if body.get("type") == "0":
        return ok({
            "processingDate": "2024-10-30 09:35:59 VET",
            "infoMsg": {
                "guId": "586f1cfc-4f33-4766-90f5-2c453e3b1fdd",
                "channel": "017", "subchannel": "01", "applId": "AVB",
                "applVersion": "0.0", "personId": "0000476138",
                "tarj_or_user": "jperez", "token": "", "action": "ListaProductos"
            },
            "code": 0,
            "message": "TRANSACCION EXITOSA",
            "productList": [{
                "productNumber": 1050136961136063536,
                "productTypeCode": "CTCTE",
                "productName": "CUENTA CORRIENTE B.M.",
                "relatedCompanyCode": "BM001",
                "currentBalance": 999999999.00
            }]
        })
    return ok({
        "processingDate": "2024-10-30 09:39:58 VET",
        "infoMsg": {
            "guId": "0b40925b-892d-486e-b1a4-9b6f4ae852eb",
            "channel": "017", "subchannel": "01", "applId": "AVB",
            "applVersion": "0.0", "personId": "8187796",
            "userId": "6820968", "token": "", "action": "ListaProductos"
        },
        "code": 50,
        "message": "NO SE TIENE INFORMACION REGISTRADA."
    })


@app.post("/conversation-starter")
def conversation_starter():
    return ok({
        "processingDate": "2024-10-21 15:48:58 VET",
        "infoMsg": {
            "guId": "d86e6eb7-efbf-4f8c-ad76-e36df5e13a3d",
            "channel": "017", "subchannel": "01", "applId": "AVB",
            "applVersion": "0.0", "personId": "0006486342",
            "userId": "servermia", "token": "", "action": "InicioConversacion"
        },
        "code": 0,
        "clientName": "PRUEBAS QA",
        "clientLastName": "CALIDAD QA",
        "personId": 6486342,
        "emailPersonal": "6054.BANCOMERCANTIL@GMAIL.COM",
        "celCodNumber": "414",
        "celNumber": 4234253,
        "birthDate": "22/03/1980",
        "birthDay": False
    })


@app.post("/consult-affiliates")
def consult_affiliates():
    return ok({
        "processingDate": "2026-05-05 15:32:29 VET",
        "infoMsg": {
            "guId": "586f1cfc-4f33-4766-90f5-2c453e3b1fdd",
            "channel": "017", "subchannel": "01", "applId": "AVB",
            "applVersion": "0.0", "personId": "0000476138",
            "tarjOrUser": "jperez", "token": "", "action": "ConsultaAfiliacionesMIA"
        },
        "code": 0,
        "groupCode": 0,
        "consultedRecords": 1,
        "consultExtended": [{
            "beneficiaryIdentificationType": "V",
            "beneficiaryIdentificationNumber": 11488316,
            "consecutive": "0", "channelCode": "6",
            "bankCode": 108, "CodPhone": 412,
            "NumPhone": 9051111, "Alias": "Jesus"
        }]
    })


@app.post("/send-tpago")
def send_tpago():
    body = parse_body()
    tpayment = body.get("TPayment", {})
    required = ["transactionAmount", "accountNumberOrigin",
                "destinationIdentificationNumber", "destinationPhoneNumber"]
    missing = [f for f in required if not tpayment.get(f)]
    if missing:
        return ok({
            "processingDate": "2026-04-29 12:09:58 VET",
            "infoMsg": {"action": "EnvioTpagoMia"},
            "code": 9999,
            "message": "Error en los datos",
            "missing_fields": missing
        })
    return ok({
        "processingDate": "2026-04-29 12:09:58 VET",
        "infoMsg": {
            "guId": "90f0ce2a-5d5f-4fd7-b0dc-1e1d71e5aa8d",
            "channel": "017", "subchannel": "01", "applId": "AVB",
            "applVersion": "1.0", "personId": "0000476138",
            "userId": "18234394", "token": "", "action": "EnvioTpagoMia"
        },
        "code": 0,
        "confirmationNumber": 48310026919,
        "fee": 0.13,
        "transactionDate": "2026-04-29T12:09:58.157",
        "transactionTime": "2026-04-29T12:09:58.157",
        "operationPassword": 26919,
        "simf": False,
        "codeF": 0
    })


@app.route("/debug", methods=["GET", "POST"])
def debug():
    raw = request.get_data(as_text=True)
    body = parse_body()
    return ok({
        "content_type": request.content_type,
        "raw_preview": raw[:300],
        "parsed_body": body,
        "type_val": body.get("type"),
        "es_igual_a_0": body.get("type") == "0"
    })
