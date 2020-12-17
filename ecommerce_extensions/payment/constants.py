""" Module for custom status of basket and exceptions. """
from oscar.apps.payment.exceptions import GatewayError

PENDING_STATUS = 'PENDING'
DECLINED_STATUS = 'DECLINED'


class InvalidEdnxDecision(GatewayError):
    """The decision returned by ednx was not recognized."""


class TransactionPending(Exception):
    """Exception for when a payment status is pending"""
