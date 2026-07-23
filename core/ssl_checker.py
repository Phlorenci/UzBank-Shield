import socket
import ssl
from datetime import datetime


def check_ssl_certificate(domain):
    if domain.startswith("http://"):
        domain = domain.replace("http://", "")

    if domain.startswith("https://"):
        domain = domain.replace("https://", "")

    domain = domain.split("/")[0]

    try:

        context = ssl.create_default_context()

        with socket.create_connection((domain, 443), timeout=5) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=domain
            ) as secure_socket:

                certificate = secure_socket.getpeercert()

        expires = datetime.strptime(
            certificate["notAfter"],
            "%b %d %H:%M:%S %Y %Z"
        )

        days_remaining = (
            expires - datetime.now()
        ).days

        issuer = dict(
            x[0]
            for x in certificate["issuer"]
        )

        return {
            "valid": True,
            "issuer": issuer.get("organizationName", "Unknown"),
            "expires": expires.strftime("%Y-%m-%d"),
            "days_remaining": days_remaining,
            "error": None
        }

    except Exception as error:

        return {
            "valid": False,
            "issuer": None,
            "expires": None,
            "days_remaining": None,
            "error": str(error)
        }