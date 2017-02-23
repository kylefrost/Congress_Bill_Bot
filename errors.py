# -*- coding: utf-8 -*-

class ProPubException(Exception):
    """Base exception for the ProPublica API"""

class UnauthorizedError(ProPubException):
    """Raise error for no API Key provided"""

class BillError(ProPubException):
    """Raise errors relating to retrieving bills"""
