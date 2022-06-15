import sys
import os
sys.path.append(os.path.join(sys.path[0], "./api"))

import grpc

import api.proto.dispenser_pb2 as dispenser_pb2
import api.proto.dispenser_pb2_grpc as dispenser_pb2_grpc

# типы message
from api.proto.dispenser_pb2 import RequestUnitMessage

from api.proto.dispenser_pb2 import ValidString
from api.proto.dispenser_pb2 import ValidUnitMessage

from api.proto.dispenser_pb2 import ResponseUnitMessage


dict_data = {
    "phone_numbers" : ['88005553535', 'LGBTelephone'],
}

def print_response(resp):
    print("info about ", resp.guid)
    if resp.msg.full_name.valid:
        print("name", resp.msg.full_name.requested_value, "is valid")
    else:
        print("name", resp.msg.full_name.requested_value, "is invalid")

    for i in resp.msg.phone_numbers:
        if i.valid:
            print("number", i.requested_value, "is valid")
        else:
            print("number", i.requested_value, "is invalid")

    for i in resp.msg.emails:
        if i.valid:
            print("email", i.requested_value, "is valid")
        else:
            print("email", i.requested_value, "is invalid")

    for i in resp.msg.addresses:
        if i.valid:
            print("address", i.requested_value, "is valid")
        else:
            print("address", i.requested_value, "is invalid")
    if resp.msg.passport_number.valid:
        print("passport", resp.msg.passport_number.requested_value, "is valid")
    else:
        print("passport", resp.msg.passport_number.requested_value, "is invalid")

    if resp.msg.passport_number.valid:
        print("birthday", resp.msg.birthday.requested_value, "is valid")
    else:
        print("birthday", resp.msg.birthday.requested_value, "is invalid")


new_data = RequestUnitMessage(**dict_data)
channel = grpc.insecure_channel('localhost:50051')
stub = dispenser_pb2_grpc.ValidationDispenserStub(channel)
response = stub.Validate(new_data)
print_response(response)