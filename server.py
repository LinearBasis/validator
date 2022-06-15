import sys
import os
from wsgiref.util import request_uri
from wsgiref.validate import validator

from numpy import full
sys.path.append(os.path.join(sys.path[0], "./api"))

from concurrent import futures

import grpc
import time

import api.proto.dispenser_pb2 as dispenser_pb2
import api.proto.dispenser_pb2_grpc as dispenser_pb2_grpc

# типы message
from api.proto.dispenser_pb2 import RequestUnitMessage

from api.proto.dispenser_pb2 import ValidString
from api.proto.dispenser_pb2 import ValidUnitMessage

from api.proto.dispenser_pb2 import ResponseUnitMessage


from validator_class import Validator


class ValidatorDispenserServide(dispenser_pb2_grpc.ValidationDispenserServicer):
    def __init__(self) -> None:
        super().__init__()
        self.guid = 1
        self.__validator : Validator = Validator()
    
    def __request_to_dict(self, request : RequestUnitMessage):
        request_dict = {
            "full_name" : request.full_name,
            "phone_numbers" : request.phone_numbers,
            "emails" : request.emails,
            "addresses" : request.addresses,
            "passport_number" : request.passport_number,
            "birthday" : request.birthday
        }
        return request_dict
    
    def __dict_to_valid_dict(self, req_dict):
        x = self.__validator.validate_all(req_dict)
        return x


    # переписать нахуй
    def __get_valid_list(self, for_what):
        x = []

        for i in for_what:
            tmp = ValidString()
            tmp.requested_value = i
            tmp.valid = for_what[i]
            x.append(tmp)
        return x


    def __get_valid_string(self, for_what):
        print(for_what)
        x = ValidString()
        x.requested_value = list(for_what.keys())[0]
        x.valid = list(for_what.values())[0]
        return x


    def __valid_dict_to_valid_message(self, valid_dict):
        dict_value = {}
        dict_value['full_name'] = None
        dict_value['phone_numbers'] = None
        dict_value['emails'] = None
        dict_value['addresses'] = None
        dict_value['passport_number'] = None
        dict_value['birthday'] = None


        if valid_dict.get('full_name'):
            dict_value['full_name'] = self.__get_valid_string(valid_dict['full_name'])
        if valid_dict.get('phone_numbers'):
            dict_value['phone_numbers'] = self.__get_valid_list(valid_dict['phone_numbers'])
        if valid_dict.get('emails'):
            dict_value['emails'] = self.__get_valid_list(valid_dict['emails'])
        if valid_dict.get('addresses'):
            dict_value['addresses'] = self.__get_valid_list(valid_dict['addresses'])
        if valid_dict.get('passport_number'):
            dict_value['passport_number'] = self.__get_valid_string(valid_dict['passport_number'])
        if valid_dict.get('birthday'):
            dict_value['birthday'] = self.__get_valid_string(valid_dict['birthday'])
        print("\n\n\n\n\n\n\n")
        for i in dict_value:
            print(i, dict_value[i])
        print(dict_value['full_name'].valid)
        print(dict_value['full_name'])
        x = ValidUnitMessage(
            full_name=dict_value['full_name'],
            phone_numbers=dict_value['phone_numbers'],
            emails=dict_value['emails'],
            addresses=dict_value['addresses'],
            passport_number=dict_value['passport_number'],
            birthday=dict_value['birthday']
        )
        return x

    def Validate(self, request : RequestUnitMessage, context):
        print("приняты данные:")
        print(request)
        print("\n\n\n\n\n\n")
        a = self.__request_to_dict(request)
        print("a is ")
        print(a)
        print("\n\n\n\n\n\n")
        b = self.__dict_to_valid_dict(a)
        print("b is ", b)
        c = self.__valid_dict_to_valid_message(b)
        ans = ResponseUnitMessage(
            guid = self.guid,
            msg=c
        )
        # ans.guid = self.guid
        self.guid += 1
        # ans.msg = c
        return ans
        # return super().Validate(request, context)




server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
dispenser_pb2_grpc.add_ValidationDispenserServicer_to_server(
    ValidatorDispenserServide(), server
)




print("starting server. listening on port 50051")
server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
