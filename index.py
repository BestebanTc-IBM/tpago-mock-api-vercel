import json
import re
from flask import Flask, request, Response

app = Flask(__name__)


def parse_body():
    """
    Lee el body crudo y extrae campos JSON sin importar el formato.
    Acepta: JSON valido, JSON con trailing commas, texto plano con pares key:value,
    fragmentos como '"type": "0"' sin llaves, prefijo 'json' de Postman.
    """
    try:
        raw = request.get_data(as_text=True).strip()
    except Exception:
        return {}
    if not raw:
        return {}

    # Quitar prefijo "json" de Postman en modo Text
    raw = re.sub(r"^json\s*", "", raw, flags=re.IGNORECASE).strip()

    # Quitar trailing commas antes de parsear
    cleaned = re.sub(r",\s*([\}\]])", r"\1", raw)

    # Intento 1: JSON valido normal
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # Intento 2: el body no tiene llaves — envolverlo en {} y parsear
    # Ejemplo: '"type": "0"' -> '{"type": "0"}'
    try:
        wrapped = "{" + cleaned.strip().strip(",") + "}"
        return json.loads(wrapped)
    except Exception:
        pass

    # Intento 3: extraccion por regex de pares "key": "value" o "key": number/bool
    result = {}
    for match in re.finditer(r'"([^"]+)"\s*:\s*("(?:[^"\\]|\\.)*"|\d+(?:\.\d+)?|true|false|null)', raw):
        key = match.group(1)
        val_str = match.group(2)
        try:
            result[key] = json.loads(val_str)
        except Exception:
            result[key] = val_str
    return result


def ok(data):
    return Response(json.dumps(data), status=200, mimetype="application/json")


# ── Endpoints ────────────────────────────────────────────────────────────────

import base64

@app.post("/spy/consultar-cuenta-principal")
def spy_consultar_cuenta_principal():
    """Endpoint SPY: devuelve el raw body exacto con analisis forense de bytes."""
    raw_bytes = request.get_data()
    raw_str = raw_bytes.decode("utf-8", errors="replace")
    b64 = base64.b64encode(raw_bytes).decode("ascii")
    hex_bytes = raw_bytes.hex()

    # Analisis caracter por caracter
    char_analysis = []
    for i, b in enumerate(raw_bytes):
        char_analysis.append({
            "pos": i,
            "byte": b,
            "hex": format(b, "02x"),
            "char": chr(b) if 32 <= b < 127 else f"<{b}>"
        })

    return ok({
        "spy": True,
        "endpoint": "/consultar-cuenta-principal",
        "content_type": request.content_type,
        "content_length": request.content_length,
        "raw_body_string": raw_str,
        "raw_body_base64": b64,
        "raw_body_hex": hex_bytes,
        "raw_body_bytes_count": len(raw_bytes),
        "char_by_char": char_analysis,
        "contains_type_0_with_space": b'"type": "0"' in raw_bytes,
        "contains_type_0_no_space": b'"type":"0"' in raw_bytes,
        "contains_backslash": b'\\' in raw_bytes,
        "headers": {k: v for k, v in request.headers if k not in ("X-Vercel-Oidc-Token", "X-Vercel-Proxy-Signature")}
    })


@app.post("/spy/send-tpago")
def spy_send_tpago():
    """Endpoint SPY: devuelve el raw body exacto para send-tpago."""
    raw_bytes = request.get_data()
    raw_str = raw_bytes.decode("utf-8", errors="replace")
    b64 = base64.b64encode(raw_bytes).decode("ascii")
    body = parse_body()
    return ok({
        "spy": True,
        "endpoint": "/send-tpago",
        "content_type": request.content_type,
        "raw_body_string": raw_str,
        "raw_body_base64": b64,
        "raw_body_hex": raw_bytes.hex(),
        "raw_body_bytes_count": len(raw_bytes),
        "contains_backslash": b'\\' in raw_bytes,
        "parsed_TPayment": body.get("TPayment"),
        "parsed_infoMsg": body.get("infoMsg"),
        "headers": {k: v for k, v in request.headers if k not in ("X-Vercel-Oidc-Token", "X-Vercel-Proxy-Signature")}
    })


@app.post("/consultar-cuenta-principal")
def consultar_cuenta_principal():
    # Orchestrate manda: {"type":"0"} sin espacio
    # El banco real requiere: "type": "0" con espacio
    # Nuestra API acepta ambos para que el agente funcione
    raw = request.get_data(as_text=True)
    body = parse_body()
    type_val = body.get("type")
    if type_val == "0":
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
