function docReady(fn) {
    // Check if DOM is already available:
    if (document.readyState === "complete" || document.readyState === "interactive") {
        // Call on next available tick
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
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
    var t0 = new Date().getTime();
    var payload = JSON.parse(formPayloadField.value);

    console.log(payload);

    function onScanSuccess(decodedText, decodedResult) {

        var t1 = new Date().getTime();

        // Parse new payload if different of previous or repeated scan are allowed and scan delay is respected:
        if (((decodedText !== lastResult) || formRepeatScanField.checked) && (t1 > t0 + formScanDelayField.value * 1000.)) {

            // Update counters:
            ++countResults;
            t0 = t1;
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

            // Async submit to process:
            $.ajax({
                url: application_target_url,
                type: application_request_mode,
                data: JSON.stringify(payload),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
            }).done(function(data) {
                console.log(data);
            });

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
