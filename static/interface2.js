var languages_names = $.getJSON("https://tools-static.wmflabs.org/tooltranslate/data/languages.json", function (data) {
    return data.languages;
});

async function addILdropdown(target) {
    var url = "https://tools-static.wmflabs.org/tooltranslate/data/petscan-list/toolinfo.json"
    // get data.languages
    var tool_languages = await fetch(url)
        .then(response => response.json())
        .then(data => {
            return data.languages;
        });

    console.table(tool_languages);

    var h = '';
    h += "<form class='form-inline' style='display:inline-block'>";
    h += "<select class='form-control custom-select'>";

    for (var lang of tool_languages) {
        var lang_name = languages_names[lang] || lang;
        h += "<option value='" + lang + "'";
        // if (lang == me.language) h += " selected";
        h += ">" + lang_name + "</option>";
    }
    h += "</select>";
    h += "&nbsp;<a href='https://tooltranslate.toolforge.org/#tool=petscan-list' target='_blank' style='text-decoration:none;font-size:2rem;vertical-align:middle;'>&#x1f30d;</a>";
    h += "</form>";
    target.html(h);

}


$(document).ready(function () {
    var tt = new ToolTranslation({
        tool: 'petscan-list',
        language: "ar",
        fallback: "en",
        highlight_missing: true,
        callback: function () {
            tt.addILdropdown($('#interface_language_wrapper'));
        }
    });
    // ---
    // wait 1 second before doing next
    setTimeout(function () {
        $('#interface_language_wrapper>form>a').hide();
    }, 1000);
});
