function docReady(fn) {
    // Check if DOM is already available:
    if (document.readyState === "complete" || document.readyState === "interactive") {
        // Call on next available tick
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

function escape(htmlStr) {
   return htmlStr.replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#39;");

}

docReady(function() {

    var formatContainer = document.getElementById('qr-reader-format');
    var contentContainer = document.getElementById('qr-reader-content');
    var scannedContainer = document.getElementById('qr-reader-scanned');
    var lastResult, countResults = 0;

    function onScanSuccess(decodedText, decodedResult) {
        if (decodedText !== lastResult) {

            // Filter out multiple scanning:
            ++countResults;
            lastResult = decodedText;
            console.log(`Scan result ${decodedText}`, decodedResult);

            // Update Interface:
            formatContainer.innerHTML = decodedResult["result"]["format"]["formatName"];
            contentContainer.innerHTML = lastResult;

            // Submit to process:
            $.ajax({
                url: qrcode_process_url,
                type: "POST",
                data: JSON.stringify(decodedResult),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
            }).done(function(data) {
                console.log(data);
                scannedContainer.innerHTML = escape(JSON.stringify(data["result"], null, 2));
            });

        }
    }

    var html5QrcodeScanner = new Html5QrcodeScanner(
        "qr-reader", {fps: 10, qrbox: 200}
    );
    html5QrcodeScanner.render(onScanSuccess);

});
