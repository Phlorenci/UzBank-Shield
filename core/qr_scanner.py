"""
QR code and barcode decoding.

Pure decode logic, independent of camera capture or GUI concerns.
Given an image frame (as a numpy array, e.g. from OpenCV), attempts
to find and decode a QR code or barcode, returning its payload and
symbology type if found.
"""

from pyzbar import pyzbar


def decode_qr_from_frame(frame):
    """
    Look for a QR code or barcode in a single image frame.

    Returns a dict:
        {"found": True, "data": "<decoded string>", "symbology": "<type>"}
        if a code was detected, or
        {"found": False, "data": None, "symbology": None} if not.

    Only the first detected code is returned if multiple are present
    in the frame.
    """

    decoded_objects = pyzbar.decode(frame)

    if decoded_objects:

        obj = decoded_objects[0]
        data = obj.data.decode("utf-8", errors="replace")

        return {
            "found": True,
            "data": data,
            "symbology": obj.type
        }

    return {
        "found": False,
        "data": None,
        "symbology": None
    }