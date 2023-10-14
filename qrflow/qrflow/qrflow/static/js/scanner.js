function docReady(fn) {
    // Check if DOM is already available:
    if (document.readyState === "complete" || document.readyState === "interactive") {
        // Call on next available tick
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

function sleep(time){
    var now = new Date().getTime();
    while(new Date().getTime() < now + time){
        /* Do nothing */
    }
}

docReady(function() {

    // Bind selectors:
    var formPayloadField = document.getElementById('id_payload');
    var formRepeatScanField = document.getElementById('id_repeat_scan');
    var formScanDelayField = document.getElementById('id_scan_delay');
    var formAutoPostField = document.getElementById('id_auto_post');
    var formSubmitButton = document.getElementById('id_submit');

    document.getElementById('id_payload').readOnly = true;

    var lastResult, countResults = 0;
    var payload = JSON.parse(formPayloadField.value);

    console.log(payload);

    function onScanSuccess(decodedText, decodedResult) {

        // Parse new payload if different of previous or repeated scan are allowed:
        if ((decodedText !== lastResult) || formRepeatScanField.checked) {

            // Filter out multiple scanning:
            ++countResults;
            lastResult = decodedText;
            console.log(decodedResult);

            // Parse new payload as JSON if possible:
            try {
                data = JSON.parse(decodedText);
                if (
                    (typeof data === "string")
                    || (typeof data === "number")
                    || (typeof data === "bigint")
                    || (typeof data === "boolean")
                ) {
                    data = {"message": data};
                }
            } catch(e) {
                data = {"message": decodedText};
            }

            // Update global payload:
            payload = Object.assign({}, payload, data);
            console.log(payload);

            // Display payload:
            formPayloadField.value = JSON.stringify(payload, null, 2)

            // Scan delay:
            sleep(formScanDelayField.value * 1000.);

            // Auto post:
            if(formAutoPostField.checked) {
                formSubmitButton.click();
            }

        }
    }

    // Create scanner and bind scan callback:
    var html5QrcodeScanner = new Html5QrcodeScanner(
        "qr-reader", {fps: 10, qrbox: 200}
    );
    html5QrcodeScanner.render(onScanSuccess);

});
