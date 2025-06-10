from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .web3_connection import web3, contract_instance
from web3 import Account
import json
from datetime import datetime
import time
from .utils import generate_qr_code
from django.conf import settings

#  서버 관리용 계정 (서버 프라이빗키로 서명)
# server_private_key = "############################"
server_private_key = getattr(settings, 'SERVER_PRIVATE_KEY')
server_account = Account.from_key(server_private_key)


#  공통 에러 핸들링
def handle_api_error(e):
    return JsonResponse({'status': 'error', 'message': str(e)})


def handle_invalid_method():
    return JsonResponse({'status': 'error', 'message': 'POST 요청만 지원합니다.'})


def handle_transaction_success(tx_hash):
    return JsonResponse({
        'status': 'success',
        'transactionHash': tx_hash.hex()
    })


#  자전거 등록 API
@csrf_exempt
def register_bicycle(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)

        # 필수값 체크
        required_fields = [
            'frameNumber', 'manufacturer', 'model', 'purchaseDate',
            'manufactureYear',
            'ownerId', 'ownerName', 'ownerRRNFront', 'ownerContact',
            'weight'
        ]
        if not all(field in data for field in required_fields):
            return JsonResponse({'status': 'error', 'message': '필수 항목 누락'})

        # YYYYMMDD → Unix timestamp 변환
        try:
            dt = datetime.strptime(data['purchaseDate'], "%Y%m%d")
            purchase_ts = int(time.mktime(dt.timetuple()))
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'purchaseDate는 YYYYMMDD 형식이어야 합니다.'})

        #  manufactureYear는 정수형으로 변환
        try:
            manufacture_year = int(data['manufactureYear'])
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'manufactureYear는 숫자여야 합니다.'})

        # weight 처리
        try:
            weight_float = float(data['weight'])  # 예: 11.56
            weight_int = int(weight_float * 100)  # → 1156
            if weight_int < 0 or weight_int > 65535:
                return JsonResponse({'status': 'error', 'message': 'weight 값이 uint16 범위를 초과합니다.'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'weight는 숫자여야 합니다.'})

        #  트랜잭션 생성
        nonce = web3.eth.get_transaction_count(server_account.address)
        txn = contract_instance.functions.registerBicycle(
            data['frameNumber'],
            data['manufacturer'],
            data['model'],
            purchase_ts,
            manufacture_year,
            data['ownerId'],
            data['ownerName'],
            data['ownerRRNFront'],
            data['ownerContact'],
            weight_int
        ).build_transaction({
            'from': server_account.address,
            'nonce': nonce,
            'gas': 500000,
            'gasPrice': web3.to_wei('1', 'gwei')
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=server_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return handle_transaction_success(receipt.transactionHash)

    except Exception as e:
        return handle_api_error(e)


# 해쉬값 조회 API
@csrf_exempt
def get_registration_hash(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)
        frame_number = data.get('frameNumber')

        if not frame_number:
            return JsonResponse({'status': 'error', 'message': 'frameNumber가 필요합니다.'})

        reg_hash = contract_instance.functions.getRegistrationHash(frame_number).call()
        return JsonResponse({'status': 'success', 'registrationHash': reg_hash})

    except Exception as e:
        return handle_api_error(e)


#  수리 이력 추가 API (timestamp 수동 입력 가능)
@csrf_exempt
def add_repair_history(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)
        reg_hash = data.get('registrationHash')
        repair_cid = data.get('repairCID')
        timestamp = data.get('timestamp')  # 옵션 필드

        if not reg_hash or not repair_cid:
            return JsonResponse({'status': 'error', 'message': 'registrationHash와 repairCID는 필수입니다.'})

        # timestamp가 없으면 현재 시각으로 설정
        if not timestamp:
            import time
            timestamp = int(time.time())

        nonce = web3.eth.get_transaction_count(server_account.address)
        txn = contract_instance.functions.addRepairHistory(reg_hash, repair_cid, timestamp).build_transaction({
            'from': server_account.address,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': web3.to_wei('1', 'gwei')
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=server_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return handle_transaction_success(receipt.transactionHash)

    except Exception as e:
        return handle_api_error(e)


#  보험 이력 추가 API (timestamp 수동 입력 가능)
@csrf_exempt
def add_insurance_history(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)
        reg_hash = data.get('registrationHash')
        insurance_cid = data.get('insuranceCID')
        timestamp = data.get('timestamp')  # 옵션 파라미터

        if not reg_hash or not insurance_cid:
            return JsonResponse({'status': 'error', 'message': 'registrationHash와 insuranceCID는 필수입니다.'})

        # timestamp가 없으면 현재 시각 사용
        if not timestamp:
            import time
            timestamp = int(time.time())

        nonce = web3.eth.get_transaction_count(server_account.address)
        txn = contract_instance.functions.addInsuranceHistory(reg_hash, insurance_cid, timestamp).build_transaction({
            'from': server_account.address,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': web3.to_wei('1', 'gwei')
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=server_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return handle_transaction_success(receipt.transactionHash)

    except Exception as e:
        return handle_api_error(e)


#  교체 이력 추가 API (timestamp 수동 입력 가능)
@csrf_exempt
def add_replacement_history(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)
        reg_hash = data.get('registrationHash')
        replacement_cid = data.get('replacementCID')
        timestamp = data.get('timestamp')  # 수동 입력 가능

        if not reg_hash or not replacement_cid:
            return JsonResponse({'status': 'error', 'message': 'registrationHash와 replacementCID는 필수입니다.'})

        # timestamp 미입력 시 현재 시각으로 처리
        if not timestamp:
            import time
            timestamp = int(time.time())

        nonce = web3.eth.get_transaction_count(server_account.address)
        txn = contract_instance.functions.addReplacementHistory(reg_hash, replacement_cid, timestamp).build_transaction(
            {
                'from': server_account.address,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': web3.to_wei('1', 'gwei')
            })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=server_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return handle_transaction_success(receipt.transactionHash)

    except Exception as e:
        return handle_api_error(e)


#  튜닝 이력 추가 API (timestamp 수동 입력 가능)
@csrf_exempt
def add_tuning_history(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)
        reg_hash = data.get('registrationHash')
        tuning_cid = data.get('tuningCID')
        timestamp = data.get('timestamp')  # 옵션 필드

        if not reg_hash or not tuning_cid:
            return JsonResponse({'status': 'error', 'message': 'registrationHash와 tuningCID는 필수입니다.'})

        # timestamp가 없으면 현재 시각으로 설정
        if not timestamp:
            import time
            timestamp = int(time.time())

        nonce = web3.eth.get_transaction_count(server_account.address)
        txn = contract_instance.functions.addTuningHistory(reg_hash, tuning_cid, timestamp).build_transaction({
            'from': server_account.address,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': web3.to_wei('1', 'gwei')
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=server_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return handle_transaction_success(receipt.transactionHash)

    except Exception as e:
        return handle_api_error(e)


#  소유권 이전 API (timestamp 수동 입력 가능)
@csrf_exempt
def transfer_ownership(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)

        reg_hash = data.get('registrationHash')
        new_owner_id = data.get('newOwnerId')
        new_owner_name = data.get('newOwnerName')
        new_owner_rrn_front = data.get('newOwnerRRNFront')
        new_owner_contact = data.get('newOwnerContact')
        timestamp = data.get('timestamp')  # 선택 입력

        if not all([reg_hash, new_owner_id, new_owner_name, new_owner_rrn_front, new_owner_contact]):
            return JsonResponse({'status': 'error', 'message': 'registrationHash 및 새 소유자 정보가 모두 필요합니다.'})

        # timestamp 없으면 현재 시각으로 설정
        if not timestamp:
            import time
            timestamp = int(time.time())

        nonce = web3.eth.get_transaction_count(server_account.address)
        txn = contract_instance.functions.transferOwnership(
            reg_hash,
            new_owner_id,
            new_owner_name,
            new_owner_rrn_front,
            new_owner_contact,
            timestamp
        ).build_transaction({
            'from': server_account.address,
            'nonce': nonce,
            'gas': 400000,
            'gasPrice': web3.to_wei('1', 'gwei')
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=server_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return handle_transaction_success(receipt.transactionHash)

    except Exception as e:
        return handle_api_error(e)


#  도난 여부 설정 API (registrationHash 기반)
@csrf_exempt
def report_stolen(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)

        reg_hash = data.get('registrationHash')
        is_stolen = data.get('isStolen')

        if reg_hash is None or is_stolen is None:
            return JsonResponse({'status': 'error', 'message': 'registrationHash와 isStolen은 필수입니다.'})

        nonce = web3.eth.get_transaction_count(server_account.address)
        txn = contract_instance.functions.reportStolen(
            reg_hash,
            bool(is_stolen)
        ).build_transaction({
            'from': server_account.address,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': web3.to_wei('1', 'gwei')
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=server_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return handle_transaction_success(receipt.transactionHash)

    except Exception as e:
        return handle_api_error(e)


#  자전거 정보 조회 API (registrationHash 직접 받는 버전)
@csrf_exempt
def get_bicycle_info(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)
        reg_hash = data.get('registrationHash')

        if not reg_hash:
            return JsonResponse({'status': 'error', 'message': 'registrationHash가 필요합니다.'})

        #  스마트컨트랙트로부터 정보 조회
        info = contract_instance.functions.getBicycleBasicInfo(reg_hash).call()

        response_data = {
            "frameNumber": info[0],
            "manufacturer": info[1],
            "model": info[2],
            "purchaseDate": info[3],
            "purchaseDateFormatted": datetime.fromtimestamp(info[3]).strftime('%Y-%m-%d'),
            "manufactureYear": info[4],  # ✅ 추가
            "registrationDate": info[5],
            "registrationDateFormatted": datetime.fromtimestamp(info[5]).strftime('%Y-%m-%d'),
            "ownerId": info[6],
            "ownerName": info[7],
            "ownerRRNFront": info[8],
            "ownerContact": info[9],
            "isStolen": info[10],
            "weight": round(info[11] / 100, 2),

        }

        return JsonResponse({"status": "success", "data": response_data})

    except Exception as e:
        return handle_api_error(e)


# 수리이력 조회 API
@csrf_exempt
def get_repair_history(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)
        reg_hash = data.get('registrationHash')

        if not reg_hash:
            return JsonResponse({'status': 'error', 'message': 'registrationHash가 필요합니다.'})

        history = contract_instance.functions.getRepairHistory(reg_hash).call()

        result = [
            {"cid": item[0], "timestamp": item[1]}
            for item in history
        ]

        return JsonResponse({"status": "success", "count": len(result), "data": result})

    except Exception as e:
        return handle_api_error(e)


# 튜닝이력 조회 API
@csrf_exempt
def get_tuning_history(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)
        reg_hash = data.get('registrationHash')

        if not reg_hash:
            return JsonResponse({'status': 'error', 'message': 'registrationHash가 필요합니다.'})

        history = contract_instance.functions.getTuningHistory(reg_hash).call()

        result = [
            {"cid": item[0], "timestamp": item[1]}
            for item in history
        ]

        return JsonResponse({"status": "success", "count": len(result), "data": result})

    except Exception as e:
        return handle_api_error(e)


# 교제이력 조회 API
@csrf_exempt
def get_replacement_history(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)
        reg_hash = data.get('registrationHash')

        if not reg_hash:
            return JsonResponse({'status': 'error', 'message': 'registrationHash가 필요합니다.'})

        history = contract_instance.functions.getReplacementHistory(reg_hash).call()

        result = [
            {"cid": item[0], "timestamp": item[1]}
            for item in history
        ]

        return JsonResponse({"status": "success", "count": len(result), "data": result})

    except Exception as e:
        return handle_api_error(e)


# 보험이력 조회 API
@csrf_exempt
def get_insurance_history(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)
        reg_hash = data.get('registrationHash')

        if not reg_hash:
            return JsonResponse({'status': 'error', 'message': 'registrationHash가 필요합니다.'})

        history = contract_instance.functions.getInsuranceHistory(reg_hash).call()

        result = [
            {"cid": item[0], "timestamp": item[1]}
            for item in history
        ]

        return JsonResponse({"status": "success", "count": len(result), "data": result})

    except Exception as e:
        return handle_api_error(e)


# 소유자이전이력 조회 API
@csrf_exempt
def get_ownership_history(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        data = json.loads(request.body)
        reg_hash = data.get('registrationHash')

        if not reg_hash:
            return JsonResponse({'status': 'error', 'message': 'registrationHash가 필요합니다.'})

        history = contract_instance.functions.getOwnershipHistory(reg_hash).call()

        result = [
            {
                "newOwnerId": item[0],
                "newOwnerName": item[1],
                "newOwnerRRNFront": item[2],
                "newOwnerContact": item[3],
                "timestamp": item[4]
            }
            for item in history
        ]

        return JsonResponse({"status": "success", "count": len(result), "data": result})

    except Exception as e:
        return handle_api_error(e)


# 등록된 모든 차대번호 조회 API
@csrf_exempt
def get_all_bicycles(request):
    if request.method != 'POST':
        return handle_invalid_method()

    try:
        frame_numbers = contract_instance.functions.getAllRegisteredFrameNumbers().call()
        return JsonResponse({"status": "success", "data": frame_numbers})

    except Exception as e:
        return handle_api_error(e)


# qr생성 api
@csrf_exempt
def generate_qr(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reg_hash = data.get("registrationHash")

            if not reg_hash:
                return JsonResponse({"error": "registrationHash가 필요합니다."}, status=400)

            filename = f"{reg_hash}.png"
            qr_path = generate_qr_code(reg_hash, filename=filename)

            return JsonResponse({
                "message": "QR 코드 생성 성공",
                "qr_code_path": qr_path
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

