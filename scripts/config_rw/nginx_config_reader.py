#!/usr/bin/env python

"""
This class contains some methods for reading and parsing file "nginx.conf".
"""

__author__ = 'Alexey Kutepov'

import re


class NginxConfigReader:
    def __init__(self):

        #Initialization of patterns:

        self.pattern_easy = re.compile('^\s*[^\#]+;{1}$')
        self.pattern_block = re.compile('^\s*[^\#]+\{{1}$')
        self.pattern_block_end = re.compile('^\s*\}{1}$')
        self.pattern_ignore = re.compile('^\s*#+.*\n+$')

#   Parsing file "nginx.conf"
#   parameter "config" contains text of the file "nginx.conf"
#   parameter "index" is position in the text in parameter "config"
    def config_handler(self, config, index=0):
        buffer = ""
        result = {}
        while index < len(config):
            buffer += config[index]
            if self.pattern_ignore.match(buffer): #pattern_ignore
                buffer = ""
                continue
            elif self.pattern_easy.match(buffer): #pattern_easy
                buffer = buffer.strip()
                result[buffer.split()[0]] = ' '.join(buffer.split()[1:])[:-1]
                buffer = ""
            elif self.pattern_block.match(buffer): #pattern_block
                index += 1
                response = self.config_handler(config, index)
                buffer = buffer.strip()
                key = ' '.join(buffer.split()[0:-1])

#               If the resulting dictionary contains the specified key,
#               it is necessary that key value stored in the list.

                if key in result:
                    item_of_result = result[key]
                    if type(item_of_result) is list:
                        item_of_result.append(response[0])
                        result[key] = item_of_result
                    else:
                        new_list = [item_of_result, response[0]]
                        result[key] = new_list
                else:
                    if key == "server": # if we found block "server"
                        result[key] = [response[0],]
                    else:
                        result[key] = response[0]

                index = response[1]
                buffer = ""
            elif self.pattern_block_end.match(buffer): #pattern_block_end
                return [result, index+1]
            index += 1
        return [result, index]

#   Reading file "nginx.conf"
    def read(self, path):
        result = {}
        file = open(path)
        config = ''.join(file.readlines())
        result['main']=(self.config_handler(config))[0]
        return result


if __name__=='__main__':
    reader = NginxConfigReader()
    path = raw_input("Enter the path to file: ")
    print reader.read(path)