$(function () {
    $("#title").autocomplete({
        source: function (request, response) {
            var wiki = $("#wiki").val(); // moved inside the function to get updated value
            $.ajax({
                url: "https://" + wiki + "/w/api.php",
                timeout: 5000,
                beforeSend: function () {
                    $("#loading").show();
                    // $("#notloading").hide();
                },
                error: function (xhr, status, error) {
                    console.error("API request failed:", error.toString().replace(/[<>'"]/g, ''));
                    response([]);
                },
                complete: function () {
                    $("#loading").hide();
                    // $("#notloading").show();
                },
                dataType: "jsonp",
                data: {
                    action: "opensearch",
                    format: "json",
                    search: request.term
                },
                success: function (data) {
                    response(data[1]); // قائمة العناوين المقترحة
                }
            });
        },
        minLength: 2 // يبدأ الإكمال بعد إدخال حرفين على الأقل
    });
});
