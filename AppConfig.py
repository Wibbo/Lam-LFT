"""
Reads details from the application configuration file and presents them appropriately as application parameters.
"""
import configparser
import json
import numpy as np


class AppConfig:

    @staticmethod
    def string_to_boolean(parameter_value, parameter_name='Invalid entry'):

        if parameter_value == 'True':
            return True
        elif parameter_value == 'False':
            return False
        else:
            err_msg = f'The value of {parameter_name} in the GoL ini file is {parameter_value}. '
            err_msg += f'It must be either True or False. The application cannot continue.'
            raise KeyError(err_msg)

    @staticmethod
    def validate_setting(value, min_val, max_val):
        if min_val > max_val:
            raise KeyError

        if value < min_val:
            value = min_val
        elif value > max_val:
            value = max_val

        return value

    @staticmethod
    def file_exists(file_name):
        f = None

        try:
            f = open(file_name)
        except Exception as e:
            raise e
        finally:
            if f is not None:
                f.close()

    def __init__(self, cfg_file):
        """
        Constructor for the AppConfig class.
        Reads parameters from the specified configuration file
        and presents them appropriately to the application.
        :param cfg_file: The name of the configuration file to read.
        """
        AppConfig.file_exists(cfg_file)

        cfg = configparser.ConfigParser()
        cfg.read(cfg_file)

        self.national_code = cfg['MAIN']['national_code']
        self.empty_field_default = cfg['MAIN']['empty_field_default']
        self.assembly_hall_postcode = cfg['POSTCODES']['assembly_hall']
        self.brockwell_park_postcode = cfg['POSTCODES']['brockwell_park']
        self.brixton_windmill_postcode = cfg['POSTCODES']['brixton_windmill']
