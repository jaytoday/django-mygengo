'''
myGengo API Client

LICENSE

This source file is subject to the new BSD license that came
with this package in the file LICENSE.txt. It is also available
through the world-wide-web at this URL:
http://mygengo.com/services/api/dev-docs/mygengo-code-license
If you did not receive a copy of the license and are unable to
obtain it through the world-wide-web, please send an email
to contact@mygengo.com so we can send you a copy immediately.

@category   myGengo
@package    API Client Library
@copyright  Copyright (c) 2009-2010 myGengo, Inc. (http://mygengo.com)
@license    http://mygengo.com/services/api/dev-docs/mygengo-code-license   New BSD License
'''

from ConfigParser import RawConfigParser

from .exception import MyGengoException

class Config(object):
    '''An in-memory container of the API configuration.'''

    __section_name = 'config'

    def __init__(self, config_path):
        '''Create an in-memory representation of the config.

        Read the config from `config_path`. If it is invalid, create an empty
        config representation.
        '''
        self.__parser = RawConfigParser()
        self.__parser.read(config_path)
        if not self.__parser.has_section(self.__section_name):
            self.__parser.add_section(self.__section_name)

    def get(self, name, default=None, must_exist=False):
        '''Return a parameter value.

        Return the value of a parameter `name`. If it is empty or doesn't
        exist, return `default` if `must_exist` is ``True`` or raise an
        exception.
        '''
        if self.__parser.has_option(self.__section_name, name):
            value = self.__parser.get(self.__section_name, name)
            if value:
                return value
        if must_exist:
            raise MyGengoException('Configuration field: %s is missing or empty.' %
                                   name)
        return default

    def set(self, name, value):
        '''Set a parameter value.

        Set the value of a parameter `name` to `value`. The value is changed
        only in memory.
        '''
        self.__parser.set(self.__section_name, name, value)

    def __getattr__(self, name):
        #if name == '_Config__parser':
        #    return self.__dict__[name]
        if self.__parser.has_option(self.__section_name, name):
            return self.__parser.get(self.__section_name, name)
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == '_Config__parser':
            self.__dict__[name] = value
        else:
            self.__parser.set(self.__section_name, name, value)
