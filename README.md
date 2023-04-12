# QR-Flow

## Requirements

  - Multi Organization/Tenant service
  - REST API to manage resources
  - Manage Certificates as a light-weight but secure Public Key Infrastructure
    - CA Creation + CRL Creation
    - Signed Certificate Chain
    - Revoke Certificate
    - Public Key Exposition
  - Generate several kind of QR-Code:
    - Simple payload (url, text, code)
    - Structured payload JSON (gRPC)
    - Signed structured payload (CST-like)
