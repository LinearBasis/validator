import re

from sympy import true

mail_regex = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
phone_regex = "^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d***/\- ]{7,10}$"

class Validator:
    def __init__(self) -> None:
        self.mods = set([
            "full_name",
            "phone_numbers",
            "emails",
            "addresses",
            "passport_number",
            "birthday"
        ])

        self.methods = {
            "full_name" : self.__validate_name, 
            "phone_numbers" : self.__validate_numbers,
            "emails" : self.__validate_mails,
            "addresses" : self.__validate_addresses,
            "passport_number" : self.__validate_passport,
            "birthday" :  self.__validate_bd
        }

        self.mail_regex = mail_regex
        self.phone_regex = phone_regex
        
        self.is_number = lambda num : re.match(self.phone_regex, num) is not None
        self.is_mail = lambda mail : re.match(self.mail_regex, mail) is not None

        self.russian_alphabet = "".join([
            chr(i) for i in range(ord('А'), ord('Я') + 1)
        ])
        
        self.english_alphabet = "".join([
            chr(i) for i in range(ord('A'), ord('Z') + 1)
        ])


    def validate_unit(self, x, mod):
        if mod not in self.mods:
            return {x : False}
        return self.methods[mod](x)


    def validate_all(self, all):
        ans = {}
        for i in all:
            ans[i] = self.validate_unit(all[i], i)
        return ans


    def __validate_name(self, full_name : str):
        if type(full_name) != str:
            return {full_name : False}
        
        splitted_names = full_name.split()
        
        if len(splitted_names) != 3:
            return {full_name : False}
        # проверка на ФИО с большой буквы
        for i in splitted_names:
            if i != i.capitalize():
                return {full_name : False}
            if len(i) < 2:
                return {full_name : False}
        
        is_russian = splitted_names[0][0] in self.russian_alphabet
        is_english = splitted_names[0][0] in self.english_alphabet

        if not is_russian and not is_english:
            return {full_name : False}
        
        abc = self.english_alphabet

        if is_russian:
            abc = self.russian_alphabet
        for i in splitted_names:
            for j in i:
                if j.upper() not in abc:
                    return {full_name : False}
        return {full_name : True}
    
    def __validate_numbers(self, numbers : str or list):
        dict_validated = {}
        for i in numbers:
            try:
                dict_validated[i] = self.is_number(i)
            except:
                dict_validated[i] = False
        return dict_validated

    def __validate_mails(self, mails : str or list):
        dict_validated = {}
        for i in mails:
            try:
                dict_validated[i] = self.is_mail(i)
            except:
                dict_validated[i] = False
        return dict_validated
        
    def __validate_addresses(self, addresses : str or list):
        dict_validated = {}
        for i in addresses:
            try:
                dict_validated[i] = True
            except:
                dict_validated[i] = False
        return dict_validated

    def __validate_passport(self, passport : str):
        if type(passport) != str:
            return {passport : False}
        return {passport : True}

    def __validate_bd(self, bd : str):
        dict_validated = {}
        for i in bd:
            try:
                dict_validated[i] = True
            except:
                dict_validated[i] = False
        return dict_validated
        
    


