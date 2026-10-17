# app/utils/security.py
import hmac
import hashlib
from config import settings

def verify_github_signature(payload_body: bytes, signature_header: str) -> bool:
    """
    Verifies that the incoming webhook payload was sent by GitHub
    using HMAC SHA-256 matching the configured WEBHOOK_SECRET.
    """
    if not signature_header or not settings.WEBHOOK_SECRET:
        return False

    try:
        sha_type, signature = signature_header.split("=")
        if sha_type != "sha256":
            return False
    except ValueError:
        return False

    # Compute expected signature using secret and request raw body bytes
    mac = hmac.new(
        settings.WEBHOOK_SECRET.encode("utf-8"),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = mac.hexdigest()

    # Compare signatures in constant time to prevent timing attacks
    return hmac.compare_digest(expected_signature, signature)