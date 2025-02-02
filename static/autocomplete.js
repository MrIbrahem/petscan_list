$(function () {
    $("#title").autocomplete({
        source: function (request, response) {
            var wiki = $("#wiki").val(); // moved inside the function to get updated value
            $.ajax({
                url: "https://" + wiki + "/w/api.php",
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
