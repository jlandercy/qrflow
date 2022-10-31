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

    var resultContainer = document.getElementById('qr-reader-results');
    var lastResult, countResults = 0;

    function onScanSuccess(decodedText, decodedResult) {
        if (decodedText !== lastResult) {

            // Filter out multiple scanning:
            ++countResults;
            lastResult = decodedText;
            console.log(`Scan result ${decodedText}`, decodedResult);

            // Update Interface:
            resultContainer.innerHTML = lastResult;

            // Submit to process:
            $.ajax({
                url: qrcode_process_url,
                type: "POST",
                data: JSON.stringify({"message": lastResult}),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
            }).done(function(data) {
                console.log(data);
            });

        }
    }

    var html5QrcodeScanner = new Html5QrcodeScanner(
        "qr-reader", {fps: 5, qrbox: 250}
    );
    html5QrcodeScanner.render(onScanSuccess);

});
