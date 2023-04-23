# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 MUJIN Inc.

from .version import __version__ # noqa: F401

import six
from typing import Optional 

try:
    import ujson as json  # noqa: F401
except ImportError:
    import json  # noqa: F401

try:
    from urllib import parse as urlparse  # noqa: F401
except ImportError:
    import urlparse  # noqa: F401

# use GetMonotonicTime if possible
try:
    from mujincommon import GetMonotonicTime
except ImportError:
    import time
    if hasattr(time, 'monotonic'):
        def GetMonotonicTime():
            return time.monotonic()
    else:
        def GetMonotonicTime():
            return time.time()

import logging
log = logging.getLogger(__name__)

try:
    from mujincommon import i18n
    ugettext, ungettext = i18n.GetDomain('mujinwebstackclientpy').GetTranslationFunctions()
except ImportError:
    def ugettext(message):
        return message

    def ungettext(singular, plural, n):
        return singular if n == 1 else plural

_ = ugettext


@six.python_2_unicode_compatible
class ClientExceptionBase(Exception):
    """client base exception
    """
    _message = None  # the error message, should be unicode
    
    def __init__(self, message: Optional[str]='') -> None:
        if message is not None and not isinstance(message,  six.text_type):
            message = message.decode('utf-8', 'ignore')
        self._message = message
    
    def __str__(self) -> str: 
        return u'%s: %s' % (self.__class__.__name__, self._message)
    
    def __repr__(self) -> str:
        return '<%s(message=%r)>' % (self.__class__.__name__, self._message)


@six.python_2_unicode_compatible
class APIServerError(ClientExceptionBase):
    _message = None  # the error. should be unicode
    _errorcode = None  # the error code coming from the server
    _detailInfoType = None # str, the detailed error type given errorcode
    _detailInfo = None # dcit, the detailed info
    _inputcommand = None  # the command sent to the server
    
    def __init__(self, message: str, errorcode: Optional[int]=None, inputcommand: Optional[str]=None, detailInfoType: Optional[str]=None, detailInfo: Optional[dict]=None) -> None:
        if message is not None and not isinstance(message, six.text_type):
            message = message.decode('utf-8', 'ignore')
        self._message = message
        self._errorcode = errorcode
        self._inputcommand = inputcommand
        self._detailInfoType = detailInfoType
        self._detailInfo = detailInfo
    
    def __str__(self) -> str:
        if self._message is not None:
            return _('API Server Error: %s')%self._message
        
        return _('API Server Error: Unknown')
    
    def __repr__(self):
        return '<%s(message=%r, errorcode=%r, inputcommand=%r, detailInfoType=%r, detailInfo=%r)>' % (self.__class__.__name__, self._message, self._errorcode, self._inputcommand, self._detailInfoType, self._detailInfo)
    
    @property
    def message(self) -> str:
        """The error message from server."""
        return self._message
    
    @property
    def errorcode(self):
        """The error code from server. Could be None."""
        return self._errorcode
    
    @property
    def stacktrace(self) -> str:
        """The stack trace for the error"""
        return ''
    
    @property
    def inputcommand(self) -> Optional[str]:
        """The command that was sent to the server. Could be None."""
        return self._inputcommand
    
    @property
    def detailInfoType(self) -> Optional[str]:
        """string for the detai info type"""
        return self._detailInfoType
    
    @property
    def detailInfo(self):
        """string for the detai info type"""
        return self._detailInfo

class TimeoutError(ClientExceptionBase):
    pass


class AuthenticationError(ClientExceptionBase):
    pass


class WebstackClientError(ClientExceptionBase):
    """Exeption class for errors returned by the web stack client"""
    _response = None # http response that resulted in the error

    def __init__(self, message='', response=None):
        super(WebstackClientError, self).__init__(message)
        self._response = response

    @property
    def response(self):
        """The http response that resulted in the error"""
        return self._response


class URIError(ClientExceptionBase):
    pass

class UserInterrupt(ClientExceptionBase):
    pass

class ControllerGraphClientException(ClientExceptionBase):

    _statusCode = None
    _content = None
    _response = None

    def __init__(self, message='', statusCode=None, content=None, response=None):
        super(ControllerGraphClientException, self).__init__(message)
        self._statusCode = statusCode
        self._content = content
        self._response = response

    @property
    def statusCode(self):
        return self._statusCode

    @property
    def content(self):
        return self._content

    @property
    def response(self):
        return self._response
