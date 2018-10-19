"""User fields validation module with regex"""

import re


class UserValidate:
    """
    Check user property validation
    """
    EMAIL = r'([a-zA-Z0-9]{1,}).@{1}([a-zA-Z0-9]{2,})\.([a-zA-Z]{2,})'
    PASSWORD = r'(.){8,}'
    NAME = r'([a-zA-Z]){3,}'
    PHONE_NUMBER = r'^09(\d){9}'  # TODO Make internasional phone number
    BIRTHDAY = r'((13|19)\d{2})(.*?)(((0[1-9])|(1[0-2])))(.*?)((0[1-9])|(1[0-9])|(2[0-9])|(3[0-1]))'

    @classmethod
    def email(cls, email: str) -> bool:
        """
        Validate user email
        :param email: user email as String
        :return bool: return true if user email valid else return false
        """
        return bool(re.match(cls.EMAIL, email))

    @classmethod
    def password(cls, password: str) -> bool:
        """
        Validate user password
        :param password: user password as String
        :return bool: return true if user password valid else return false
        """
        return bool(re.match(cls.PASSWORD, password))

    @classmethod
    def name(cls, name: str) -> bool:
        """
        Validate user first_name, last_name, job, city, country and bio
        :param name: user entries for first_name, last_name, job, city,
        country or bio
        :return bool: return true if entry valid else return false
        """
        return bool(re.match(cls.NAME, name))

    @classmethod
    def phone_number(cls, phone_number: str) -> bool:
        """
        Validate user phone_number
        :param phone_number: user phone number as String
        return bool: return true if phone number is valid else return false
        """
        return bool(re.match(cls.PHONE_NUMBER, phone_number))

    @classmethod
    def birthday(cls, birthday_: str) -> bool:
        """
        Validate user birthday
        :param birthday: user birthday as String
        return bool: return true if birthday is valid else return false
        """
        return bool(re.match(cls.BIRTHDAY, birthday_))
