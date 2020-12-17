from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from hashlib import sha256

import json
import requests
import uuid

@csrf_exempt
def listener(request):
    if request.method == 'POST':
        epp_request = request.POST.dict()
        return render(request, 'sandbox_listener/index.html', {'data':epp_request})


@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def landing(request):
    return HttpResponse('Sandbox for edupay')


@api_view(('GET', 'POST'))
@permission_classes((permissions.AllowAny,))
def transaction_approved(request):
    if request.method == 'POST':
        epp_request = request.POST.get('data')
        epp_request = epp_request.replace("'", '"')
        data = json.loads(epp_request)

        #-------------------POST RESPONSE------------------
        epp_post = post(data, "APPROVED")
        post_req = requests.post(data['confirmationUrl'], data = epp_post)

        redirect_url = data['confirmationUrl'].split('payment')[0]

    return redirect(redirect_url+'checkout/receipt/?order_number='+data['referenceCode'])


@api_view(('GET', 'POST'))
@permission_classes((permissions.AllowAny,))
def transaction_pending(request):
    if request.method == 'POST':
        epp_request = request.POST.get('data')
        epp_request = epp_request.replace("'", '"')
        data = json.loads(epp_request)

        #-------------------POST RESPONSE------------------
        epp_post = post(data, "PENDING")
        post_req = requests.post(data['confirmationUrl'], data = epp_post)

    return redirect(data['responseUrl'])


@api_view(('GET', 'POST'))
@permission_classes((permissions.AllowAny,))
def transaction_declined(request):
    if request.method == 'POST':
        epp_request = request.POST.get('data')
        epp_request = epp_request.replace("'", '"')
        data = json.loads(epp_request)

        #-------------------POST RESPONSE------------------
        epp_post = post(data, "DECLINED")
        post_req = requests.post(data['confirmationUrl'], data = epp_post)

    return redirect(data['responseUrl'])


def post(data, response_type):

    STATE_POL, RESPONSE_CODE_POL = status_code(response_type)

    value = data['amount']
    last_decimal = value[-1]
    if last_decimal == '0':
        new_value = value[:-1]
    else:
        new_value = value

    uncoded = "{api_key}~{merchant_id}~{reference_sale}~{new_value}~{currency}~{state_pol}".format(
        api_key='4Vj8eK4rloUd272L48hsrarnUA',
        merchant_id=data['merchantId'],
        reference_sale=data['referenceCode'],
        new_value=new_value,
        currency=data['currency'],
        state_pol=STATE_POL,
    )

    sign = sha256(uncoded.encode('utf-8')).hexdigest()

    id = uuid.uuid1()

    post_res = {
        "state_pol": STATE_POL,
        "response_code_pol": RESPONSE_CODE_POL,
        "reference_sale": data['referenceCode'],
        "reference_pol": "7069375",
        "sign": sign,
        "value": data['amount'],
        "currency": data['currency'],
        "description": "Test PP",
        "billing_address": "Calle 123",
        "billing_city": "Los Mochis",
        "billing_country": "MX",
        "transaction_id": id,
        "response_message_pol": response_type,
    }
    return post_res


def get(data, response_type):

    STATE_POL, RESPONSE_CODE_POL = status_code(response_type)

    id = uuid.uuid1()

    get_res = {
        "merchantId": data['merchantId'],
        "merchant_name": "Test Name",
        "merchant_address": "Calle 123",
        "telephone": "7512354",
        "merchant_url": "http://localhost:18133/sandbox/",
        "transactionState": STATE_POL,
        "lapTransactionState": response_type,
        "message": response_type,
        "referenceCode": data['referenceCode'],
        "reference_pol": "7069375",
        "transactionId": id,
        "description": "test_ednxPP",
        "trazabilityCode": "" ,
        "cus": "" ,
        "orderLanguage": "es",
        "extra1": "" ,
        "extra2": "" ,
        "extra3": "" ,
        "polTransactionState": STATE_POL,
        "signature": data['signature'],
        "polResponseCode": RESPONSE_CODE_POL,
        "lapResponseCode": response_type,
        "risk": "1.00",
        "cc_number": "4444333322221111",
        "polPaymentMethod": "10",
        "lapPaymentMethod": "VISA",
        "polPaymentMethodType": "2",
        "lapPaymentMethodType": "CREDIT_CARD",
        "installmentsNumber": "1",
        "TX_VALUE": data['amount'],
        "TX_TAX": ".00",
        "currency": data['currency'],
        "lng": "es",
        "pseCycle": "" ,
        "pseBank": "" ,
        "pseReference1": "" ,
        "pseReference2": "" ,
        "pseReference3": "" ,
        "authorizationCode": "" ,
        "TX_ADMINISTRATIVE_FEE": ".00",
        "TX_TAX_ADMINISTRATIVE_FEE": ".00",
        "TX_TAX_ADMINISTRATIVE_FEE_RETURN_BASE": ".00",
    }

    return get_res


def status_code(response_type):
    STATE_POL = "0"
    RESPONSE_CODE_POL = "0"
    if response_type == 'APPROVED':
        STATE_POL = "4"
        RESPONSE_CODE_POL = "1"
    elif response_type == 'PENDING':
        STATE_POL = "7"
        RESPONSE_CODE_POL = "25"
    elif response_type == 'DECLINED':
        STATE_POL = "6"
        RESPONSE_CODE_POL = "104"

    return STATE_POL, RESPONSE_CODE_POL
