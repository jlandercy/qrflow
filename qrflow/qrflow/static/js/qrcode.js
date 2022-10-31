function update_qrcode(context) {

    console.log(context)

    var message = {
        "message": $(this).val()
    };
    //console.log(message);

    $.ajax({
        url: url,
        type: "POST",
        data: JSON.stringify(message),
        contentType: "application/json; charset=utf-8",
        dataType: "text",
    }).done(function(data) {
        //console.log(data);
        $("#qrcode-image").attr("src", data);
    });

}

// Trigger when document is ready:
$(document).ready(update_qrcode);

// Bind key up event as well:
$(document).ready(function(context) {
    $("#key-textbox").keyup(update_qrcode);
});
