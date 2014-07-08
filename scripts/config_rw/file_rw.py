__author__ = 'alexey'

from errors.rigery_error import RigeryError

class FileRW:


    """
        Reading file
        :parameter path - path to file
        :return text of file
        :except RigeryError
    """
    def read(self, path):
        try:
            file = open(path)
            result = ''.join(file.readlines())
            file.close()
        except IOError:
            raise RigeryError("IOError", "Unable to access the file: "+path)
        else:
            return result

    def write(self, path, text):
        try:
            file = open(path, 'w')
            file.write(text)
            file.close()
        except IOError:
            raise RigeryError("IOError", "Unable to access the file: "+path)

