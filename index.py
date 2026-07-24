from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/consultar-cuenta-principal", methods=["POST"])
def consultar_cuenta_principal():
    return jsonify({
        "processingDate": "2024-10-30 09:35:59 VET",
        "infoMsg": {
            "guId": "586f1cfc-4f33-4766-90f5-2c453e3b1fdd",
            "channel": "017",
            "subchannel": "01",
            "applId": "AVB",
            "applVersion": "0.0",
            "personId": "0000476138",
            "tarjOrUser": "jperez",
            "token": "",
            "action": "ListaProductos"
        },
        "code": 0,
        "message": "TRANSACCION EXITOSA",
        "productList": [
            {
                "productNumber": "01050136961136063536",
                "productTypeCode": "CTCTE",
                "productName": "CUENTA CORRIENTE B.M.",
                "relatedCompanyCode": "BM001",
                "currentBalance": 999999999.00
            }
        ]
    })

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
