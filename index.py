from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def get_body():
    """
    Parsea el body JSON de forma robusta.
    Maneja: Content-Type text/plain, JSON con trailing commas, whitespace extra.
    """
    import re

    raw = ""

    # Leer raw bytes primero (funciona con cualquier Content-Type)
    try:
        raw = request.data.decode("utf-8").strip()
    except Exception:
        pass

    # Si no hay datos en request.data intentar con get_json force
    if not raw:
        try:
            data = request.get_json(silent=True, force=True)
            if data is not None:
                return data
        except Exception:
            pass
        return {}

    # Limpiar trailing commas antes de parsear (JSON invalido comun)
    # Ejemplo: {"type": "0",} o {"a": 1, "b": 2,}
    clean = re.sub(r",\s*([\}\]])", r"\1", raw)

    try:
        return json.loads(clean)
    except Exception:
        pass

    return {}


@app.route("/debug", methods=["POST", "GET"])
def debug():
    """Endpoint de diagnostico para ver exactamente que recibe Vercel."""
    raw_data = request.data
    body_json = None
    parse_error = None
    try:
        body_json = json.loads(raw_data.decode("utf-8"))
    except Exception as e:
        parse_error = str(e)

    return jsonify({
        "content_type": request.content_type,
        "content_length": request.content_length,
        "raw_data_bytes": len(raw_data),
        "raw_data_preview": raw_data.decode("utf-8", errors="replace")[:500],
        "get_json_force": request.get_json(silent=True, force=True),
        "get_json_native": request.get_json(silent=True),
        "parsed_body": body_json,
        "parse_error": parse_error,
        "headers": dict(request.headers),
        "method": request.method
    })

RESPONSE_EXITOSO = {
    "processingDate": "2024-10-30 09:35:59 VET",
    "infoMsg": {
        "guId": "586f1cfc-4f33-4766-90f5-2c453e3b1fdd",
        "channel": "017",
        "subchannel": "01",
        "applId": "AVB",
        "applVersion": "0.0",
        "personId": "0000476138",
        "tarj_or_user": "jperez",
        "token": "",
        "action": "ListaProductos"
    },
    "code": 0,
    "message": "TRANSACCION EXITOSA",
    "productList": [
        {
            "productNumber": 1050136961136063536,
            "productTypeCode": "CTCTE",
            "productName": "CUENTA CORRIENTE B.M.",
            "relatedCompanyCode": "BM001",
            "currentBalance": 999999999.00
        }
    ]
}

RESPONSE_ERROR = {
    "processingDate": "2024-10-30 09:39:58 VET",
    "infoMsg": {
        "guId": "0b40925b-892d-486e-b1a4-9b6f4ae852eb",
        "channel": "017",
        "subchannel": "01",
        "applId": "AVB",
        "applVersion": "0.0",
        "personId": "8187796",
        "userId": "6820968",
        "token": "",
        "action": "ListaProductos"
    },
    "code": 50,
    "message": "NO SE TIENE INFORMACION REGISTRADA."
}

@app.route("/consultar-cuenta-principal", methods=["POST"])
def consultar_cuenta_principal():
    # La unica condicion para retornar exitoso es que type sea exactamente el string "0"
    # Cualquier otro valor (None, "", "01", "10", 0 entero, sin body) retorna code 50
    body = get_body()
    type_val = body.get("type")

    if type_val == "0":
        return jsonify(RESPONSE_EXITOSO)
    return jsonify(RESPONSE_ERROR)

@app.route("/conversation-starter", methods=["POST"])
def conversation_starter():
    return jsonify({
        "processingDate": "2024-10-21 15:48:58 VET",
        "infoMsg": {
            "guId": "d86e6eb7-efbf-4f8c-ad76-e36df5e13a3d",
            "channel": "017",
            "subchannel": "01",
            "applId": "AVB",
            "applVersion": "0.0",
            "personId": "0006486342",
            "userId": "servermia",
            "token": "",
            "action": "InicioConversacion"
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

@app.route("/consult-affiliates", methods=["POST"])
def consult_affiliates():
    return jsonify({
        "processingDate": "2026-05-05 15:32:29 VET",
        "infoMsg": {
            "guId": "586f1cfc-4f33-4766-90f5-2c453e3b1fdd",
            "channel": "017",
            "subchannel": "01",
            "applId": "AVB",
            "applVersion": "0.0",
            "personId": "0000476138",
            "tarjOrUser": "jperez",
            "token": "",
            "action": "ConsultaAfiliacionesMIA"
        },
        "code": 0,
        "groupCode": 0,
        "consultedRecords": 1,
        "consultExtended": [
            {
                "beneficiaryIdentificationType": "V",
                "beneficiaryIdentificationNumber": 11488316,
                "consecutive": "0",
                "channelCode": "6",
                "bankCode": 108,
                "CodPhone": 412,
                "NumPhone": 9051111,
                "Alias": "Jesus"
            }
        ]
    })

@app.route("/send-tpago", methods=["POST"])
def send_tpago():
    body = get_body()
    tpayment = body.get("TPayment", {})

    REQUIRED_TPAYMENT_FIELDS = [
        "transactionAmount", "accountNumberOrigin",
        "destinationIdentificationNumber", "destinationPhoneNumber"
    ]
    missing = [f for f in REQUIRED_TPAYMENT_FIELDS if not tpayment.get(f)]

    if missing:
        return jsonify({
            "processingDate": "2026-04-29 12:09:58 VET",
            "infoMsg": {"action": "EnvioTpagoMia"},
            "code": 9999,
            "message": "Error en los datos",
            "debug": {
                "campos_faltantes_en_TPayment": missing
            }
        }), 200

    return jsonify({
        "processingDate": "2026-04-29 12:09:58 VET",
        "infoMsg": {
            "guId": "90f0ce2a-5d5f-4fd7-b0dc-1e1d71e5aa8d",
            "channel": "017",
            "subchannel": "01",
            "applId": "AVB",
            "applVersion": "1.0",
            "personId": "0000476138",
            "userId": "18234394",
            "token": "",
            "action": "EnvioTpagoMia"
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

handler = app
