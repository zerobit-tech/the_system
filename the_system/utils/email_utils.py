from validate_email import validate_email,validate_email_or_fail
from typing import Optional
from ssl import SSLContext
"""
email_address: the email address to check

check_format: check whether the email address has a valid structure; defaults to True

check_blacklist: check the email against the blacklist of domains downloaded from https://github.com/disposable-email-domains/disposable-email-domains; defaults to True

check_dns: check the DNS mx-records, defaults to True

dns_timeout: seconds until DNS timeout; defaults to 10 seconds

check_smtp: check whether the email actually exists by initiating an SMTP conversation; defaults to True

smtp_timeout: seconds until SMTP timeout; defaults to 10 seconds

smtp_helo_host: the hostname to use in SMTP HELO/EHLO; if set to None (the default), the fully qualified domain name of the local host is used

smtp_from_address: the email address used for the sender in the SMTP conversation; if set to None (the default), the email_address parameter is used as the sender as well

smtp_skip_tls: skip the TLS negotiation with the server, even when available. defaults to False

smtp_tls_context: an SSLContext to use with the TLS negotiation when the server supports it. defaults to None

smtp_debug: activate smtplib's debug output which always goes to stderr; defaults to False


"""


def is_valid_email(email_address):
    is_valid = True
    error_message = ''
    try:
        is_valid = validate_email_or_fail(
        email_address=email_address,
        check_format = True,
        check_blacklist = True, 
        check_dns = True,
        dns_timeout = 10, 
        check_smtp = True,
        smtp_timeout = 10, 
        smtp_helo_host = None,
        smtp_from_address = None,
        smtp_skip_tls = False, 
        smtp_tls_context = None,
        smtp_debug = False
        )
    except Exception as e:
       is_valid =False
       error_message = str(e)

    return (is_valid, error_message) 
    