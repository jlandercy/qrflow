import barcode

HTTP_METHODS = (
    ('HEAD', 'HEAD'),
    ('GET', 'GET'),
    ('POST', 'POST'),
    ('PUT', 'PUT'),
    ('PATCH', 'PATCH'),
    ('DELETE', 'DELETE'),
    ('OPTIONS', 'OPTIONS'),
    ('TRACE', 'TRACE'),
    ('CONNECT', 'CONNECT'),
)

SCANNER_MODES = (
    ('FORWARD', 'FORWARD'),
    ('RPC', 'RPC'),
)

CODE_TYPES = [
    ('QR', 'QR'),
    ('QR-JSON', 'QR-JSON'),
    ('QR-EPC', 'QR-EPC'),
    ('QR-DGC', 'QR-DGC'),
] + [(code, code.upper()) for code in barcode.PROVIDED_BARCODES]
