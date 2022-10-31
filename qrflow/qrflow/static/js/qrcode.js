function update_qrcode(context) {

    $.ajax({
        url: qrcode_create_url,
        type: "POST",
        data: JSON.stringify({"message": $(this).val()}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
    }).done(function(data) {
        console.log(data);
        $("#qrcode-image").attr("src", data["payload"]);
    });

}

// Trigger when document is ready:
$(document).ready(update_qrcode);

// Bind key up event as well:
$(document).ready(function(context) {
    $("#key-textbox").keyup(update_qrcode);
});
