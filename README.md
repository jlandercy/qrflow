# QR-Flow

## Requirements

  - Multi Organization/Tenant service
  - REST API to manage resources
  - Manage Certificates as a light-weight but secure Public Key Infrastructure
    - Certificate Type: CA, CRL, SDC (single domain), WC (wildcard domain), MDC (multi domain certificate)
    - CA Creation + CRL Creation
    - Signed Certificate Chain
    - Revoke Certificate
    - Public Key Exposition
  - Generate several kind of QR-Code:
    - Simulate customer logic endpoints 
    - QR-Code type:
      - Simple payload (url, text, code):
        - Scanner read it and at most a binding is sent to a single URL
      - Structured payload JSON (gRPC)
        - 
      - Signed structured payload (CST-like)
