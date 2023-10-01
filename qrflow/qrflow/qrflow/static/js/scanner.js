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

    var formPayloadField = document.getElementById('id_payload');
    var formAutoPostField = document.getElementById('id_auto_post');
    var formSubmitButton = document.getElementById('id_submit');

    document.getElementById('id_payload').readOnly = true;

    var lastResult, countResults = 0;
    var payload = JSON.parse(formPayloadField.value);

    console.log(payload);

    function onScanSuccess(decodedText, decodedResult) {

        if (decodedText !== lastResult) {

            // Filter out multiple scanning:
            ++countResults;
            lastResult = decodedText;
            console.log(decodedResult);

            try {
                data = JSON.parse(decodedText);
            } catch(e) {
                data = {"message": decodedText};
            }

            payload = Object.assign({}, payload, data);
            console.log(payload);

            formPayloadField.value = JSON.stringify(payload, null, 2)

            if(formAutoPostField.checked) {
                formSubmitButton.click();
            }

        }
    }

    var html5QrcodeScanner = new Html5QrcodeScanner(
        "qr-reader", {fps: 10, qrbox: 200}
    );
    html5QrcodeScanner.render(onScanSuccess);

});
