#!/usr/bin/env python

__author__ = 'Alexey Kutepov'

import re

class NginxConfigReader:
    def __init__(self):
        self.pattern_easy = re.compile('^\s*[^\#]+;{1}$')
        self.pattern_block = re.compile('^\s*[^\#]+\{{1}$')
        self.pattern_block_end = re.compile('^\s*\}{1}$')
        self.pattern_ignore = re.compile('^\s*#+.*\n+$')

    def config_handler(self, config, index=0):
        buffer = ""
        result = []
        while index < len(config):
            buffer += config[index]
            item = {}
            if self.pattern_ignore.match(buffer): #pattern_ignore
                buffer = ""
                continue
            elif self.pattern_easy.match(buffer): #pattern_easy
                buffer = buffer.strip()
                item[buffer.split()[0]] = ' '.join(buffer.split()[1:])[:-1]
                result.append(item)
                buffer = ""
            elif self.pattern_block.match(buffer): #pattern_block
                index += 1
                response = self.config_handler(config, index)
                buffer = buffer.strip()
                item[' '.join(buffer.split()[0:-1])] = response[0]
                result.append(item)
                index = response[1]
                buffer = ""
            elif self.pattern_block_end.match(buffer): #pattern_block_end
                return [result, index+1]
            index += 1
        return [result, index]

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