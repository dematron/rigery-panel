__author__ = 'alexey'


"""
    Exception for project Rigery panel
"""

class RigeryError(Exception):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return str(self.error_code + " : " + self.message)
