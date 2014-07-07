__author__ = 'alexey'

class NginxConfigRW:

#   Reading file "nginx.conf"
    def read(self, path):
        file = open(path)
        result = ''.join(file.readlines())
        file.close()
        return result

    def write(self, path, text):
        file = open(path, 'w')
        file.write(text)
        file.close()
