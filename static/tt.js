/*
    Always include this file as https://tools-static.wmflabs.org/tooltranslate/tt.js

    intitial_params keys are:
    - tool The name of the tool; the key in the online translation. Mandatory.
    - language Language to load; default is "interface_language" URL parameter, browser/system language, or 'en' as fallback. Optional.
    - languages Multiple languages to pre-load
    - highlight_missing Shows missing translations in the interface. true or false (default). Optional.
    - fallback A fallback language, to use if a translation string is not available. If highlight_missing==true, fallback strings will be wrapped <i>in italics</i>. Optional.
    - callback A callback function, called once translations have been loaded. Optional.
    - onUpdateInterface A custom function that is called after every interface update.
    - onLanguageChange A custom function that is called after the language was changed through the standard dropdown.
    - debug Show some console.log messages on problems. true or false (default). Optional.
*/
function ToolTranslation(intitial_params) {


    this.createCookie = function (name, value, days) {
        var expires;
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toGMTString();
        }
        else {
            expires = "";
        }
        document.cookie = name + "=" + value + expires + "; path=/";
    }

    this.getCookie = function (c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) {
                    c_end = document.cookie.length;
                }
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
        return "";
    }

    // INIT

    this.access_key_prefixes = {
        ie_win: 'Alt',
        chrome_win: 'Alt',
        chrome_linux: 'Alt',
        chrome_mac: 'Ctrl+Alt',
        firefox_win: 'Alt+Shift',
        firefox_linux: 'Alt+Shift',
        firefox_mac: 'Ctrl+Alt',
        safari_win: 'Alt',
        safari_mac: 'Ctrl+Alt'
    };

    this.rtl = ["ar", "arc", "arz", "ks", "lrc", "mzn", "azb", "nqo", "pnb", "ps", "sd", "ug", "ur", "yi", "ckb", "dv", "fa", "glk", "he"];
    this.loaded = false;
    this.toolname = intitial_params.tool;
    if (typeof this.toolname == 'undefined') {
        console.log("ToolTranslation requires parameter 'tool' with the toolname key");
        return;
    }

    if (typeof intitial_params.highlight_missing != 'undefined') this.highlight_missing = intitial_params.highlight_missing;

    this.toolinfo = {};
    this.tool_path = 'https://tools-static.wmflabs.org/tooltranslate/'; // 'https://tooltranslate.toolforge.org/' ;

    this.force_fresh = intitial_params.force_fresh ? true : false;
    this.force_fresh = true; // Caching issues on Labs :-(

    if (typeof intitial_params.fallback != 'undefined') this.fallback = intitial_params.fallback;

    this.onLanguageChange = intitial_params.onLanguageChange;

    var language_from_cookie = this.getCookie('interface_language');
    var m = window.location.href.match(/[\#\&\?]interface_language=([a-z_-]+)/);
    if (m != null) this.language = m[1];
    else if (language_from_cookie != '') this.language = language_from_cookie;
    else this.language = window.navigator.userLanguage || window.navigator.language || 'en';
    this.language = this.language.replace(/-.+$/, ''); // Main language only
    this.translation_cache = {};

    this.onUpdateInterface = function () { }; // Dummy
    if (typeof intitial_params.onUpdateInterface != 'undefined') this.onUpdateInterface = intitial_params.onUpdateInterface;

    var me = this;
    $.each(['highlight_missing', 'no_interface_update', 'debug'], function (k, v) {
        me[v] = false;
        if (typeof intitial_params[v] == 'undefined') return;
        me[v] = intitial_params[v];
    });


    // METHODS



    this.getLanguages = function () {
        var me = this;
        var ret = [];
        $.each(me.translation_cache, function (lang, dummy) {
            ret.push(lang);
        });
        return ret;
    }

    this.log = function (s) {
        if (!this.debug) return;
        console.log(s);
    }

    this.setCache = function (lang, key, text) {
        var me = this;
        if (typeof me.translation_cache[lang] == 'undefined') me.translation_cache[lang] = {};
        me.translation_cache[lang][key] = text;
    }

    this.hasLanguage = function (lang) {
        var me = this;
        if (typeof me.translation_cache[lang] == 'undefined') return false;
        return true;
    }

    this.t = function (key, options) {
        var me = this;
        if (typeof options == 'undefined') options = {};
        if (typeof options.lang == 'undefined' || options.lang == '') options.lang = me.language; // Default language, unless specified
        if (typeof me.translation_cache[options.lang] == 'undefined') return; //"LANGUAGE "+lang+" NOT LOADED" ;
        if (typeof me.translation_cache[options.lang][key] != 'undefined') {
            var ret = me.sanitizeHTML(me.translation_cache[options.lang][key]);
            if (typeof options.params != 'undefined') {
                $.each(options.params, function (k, v) {
                    ret = ret.replace('$' + (k + 1), v);
                });
            }
            if (me.highlight_missing) {
                if (options.using_fallback_language) ret = "<i>" + ret + "</i>";
            }
            return ret;
        }
        if (typeof me.fallback != 'undefined' && options.lang != me.fallback && !options.using_fallback_language) {
            var o2 = $.extend(true, {}, options);
            o2.using_fallback_language = true;
            o2.lang = me.fallback;
            return me.t(key, o2);
        }
        if (me.highlight_missing) return "<span style='font-size:7pt;color:red'>" + key + "</span>";
    }

    this.getJoinedKeys = function () {
        var me = this;
        var tmp = {};
        $.each(me.translation_cache, function (lang, v0) {
            $.each(v0, function (k, v) {
                tmp[k] = 1;
            });
        });
        var ret = [];
        $.each(tmp, function (k, v) {
            ret.push(k);
        });
        ret.sort();
        return ret;
    }


    // TODO improve, suppress all JS injection
    this.sanitizeHTML = function (s) {
        if (s === null) return 'null';
        return s.replace(/<\s*script/i, '');
    }

    this.setLanguage = function (lang, callback) {
        var me = this;
        me.language = lang;
        $('html').attr('lang', lang);
        if (me.rtl.indexOf(lang) > -1) {
            $('html').attr('dir', 'rtl');
        } else {
            $('html').attr('dir', 'ltr');
        }
        me.loadToolTranslation(lang, callback);
        me.createCookie('interface_language', lang);
    }

    this.replace_ttx = function (o, h) {
        for (var i = 1; i < 10; i++) {
            var v = o.attr('tt' + i);
            if (typeof v == 'undefined') break;
            let r = new RegExp('\\$' + i, 'g');
            h = h.replace(r, v);
        }
        return h;
    }

    this.updateInterface = function (root) {
        var me = this;
        if (typeof me.translation_cache[me.language] == 'undefined') {
            me.log("No translation for " + me.language + " was loaded");
            return;
        }

        if (typeof root == 'undefined') root = document;
        var d = me.translation_cache[me.language];

        // HTML elements
        $(root).find('[tt]').each(function (k, v) {
            var o = $(v);
            var key = o.attr('tt');
            var h = me.t(key);
            if (typeof h == 'undefined') {
                if (me.debug) console.log("No key for " + key + " in " + me.language);
                h = '';
            } else {
                h = me.replace_ttx(o, h);
            }
            o.html(h);
        });

        // title
        $(root).find('[tt_title]').each(function (k, v) {
            var o = $(v);
            var key = o.attr('tt_title');
            if (typeof d[key] == 'undefined') return;
            var a = 'title';
            if (typeof o.attr('data-original-title') != 'undefined') a = 'data-original-title'; // Bootstrap hover title
            var h = d[key];
            h = me.replace_ttx(o, h);
            o.attr(a, me.sanitizeHTML(h));
        });

        // placeholder
        $(root).find('[tt_placeholder]').each(function (k, v) {
            var o = $(v);
            var key = o.attr('tt_placeholder');
            if (typeof d[key] == 'undefined') return;
            o.attr({ placeholder: me.sanitizeHTML(d[key]) });
        });

        // value (e.g. submit button)
        $(root).find('[tt_value]').each(function (k, v) {
            var o = $(v);
            var key = o.attr('tt_value');
            if (typeof d[key] == 'undefined') return;
            o.attr({ 'value': me.sanitizeHTML(d[key]) });
        });

        // Access keys
        if (typeof window.navigator != 'undefined') {
            let os = '';
            if (/Macintosh/.test(window.navigator.userAgent)) os = 'mac';
            else if (/Windows/.test(window.navigator.userAgent)) os = 'win';
            else if (/Linux/.test(window.navigator.userAgent)) os = 'linux';

            let browser = '';
            if (/Safari/.test(window.navigator.userAgent)) browser = 'safari';
            else if (/Firefox/.test(window.navigator.userAgent)) browser = 'firefox';
            else if (/Chrome/.test(window.navigator.userAgent)) browser = 'chrome';
            else if (/Opera/.test(window.navigator.userAgent)) browser = 'opera';

            let prefix = 'Shortcut (plus crontol keys): ';
            let browser_os = browser + '_' + os;
            if (typeof me.access_key_prefixes[browser_os] != 'undefined') prefix = me.access_key_prefixes[browser_os] + '+';

            $(root).find('[accesskey]').each(function (k, v) {
                let o = $(v);
                let title = o.attr('title');
                if (typeof title != 'undefined' && /\[/.test(title)) return;
                let note = '[' + prefix + o.attr('accesskey') + ']';
                if (typeof title == 'undefined' || title == '') title = note;
                else title += ' ' + note;
                o.attr({ title: title });
            });
        }

        if (me.updating_interface) return; // Prevent recursion, if onUpdateInterface updates the interface!
        me.updating_interface = true;
        me.onUpdateInterface();
        me.updating_interface = false;
    }

    this.loadToolTranslation = function (languages, callback) {
        var me = this;
        if (typeof languages != 'object') languages = [languages]; // Enforce array
        if (typeof callback == 'undefined') callback = function () { }; // Dummy

        var l2 = [];
        $.each(languages, function (dummy, lang) {
            if (typeof me.translation_cache[lang] == 'undefined') l2.push(lang);
        });

        function and_done() {
            if (!me.no_interface_update) me.updateInterface();
            me.loaded = true;
            callback();
        }

        if (l2.length > 0) {

            var running = l2.length;
            function fin() {
                running--;
                if (running > 0) return;
                and_done();
            }

            if (typeof me.toolinfo.languages == 'undefined') {
                running++;
                $.get(me.tool_path + 'data/' + me.toolname + '/toolinfo.json', function (d) {
                    me.toolinfo = d;
                }, 'json').always(function () { fin() });
            }

            $.each(l2, function (dummy, lang) {
                // Sanitize language name
                lang = lang.replace(/[^a-z_-]/g, '');

                // Load language from cache
                var url = me.tool_path + 'data/' + me.toolname + '/' + lang + '.json';
                if (me.force_fresh) {
                    var date = new Date();
                    var n = date.getTime();
                    //					url += '#random=' + Math.random() + '.' + n ;
                }
                $.get(url, function (d) {
                    me.translation_cache[lang] = d;
                }, 'json').done(function () {
                    fin();
                }).fail(function () {
                    me.translation_cache[lang] = {};
                    me.log("Could not load translation for " + lang);
                    me.log(url);
                    fin();
                });
            });

        } else {
            and_done();
        }
    }

    this.addILdropdown = function (target) {
        var me = this;

        function addDropdown() {
            if (typeof me.toolinfo.languages == 'undefined') {
                setTimeout(function () {
                    me.addILdropdown(target);
                }, 100);
                return;
            }
            var h = '';
            h += "<form class='form-inline' style='display:inline-block'>";
            h += "<select class='form-control custom-select' data-bs-theme='auto'>";
            me.toolinfo.languages.sort();
            $.each(me.toolinfo.languages, function (dummy, language) {
                var language_name = me.language_cache[language];
                if (typeof language_name == 'undefined') language_name = language.toUpperCase(); // Fallback, in case no language name is defined
                h += "<option value='" + language + "'";
                if (language == me.language) h += " selected";
                h += ">" + language_name + "</option>";
            });
            h += "</select>";
            // h += "&nbsp;<a href='https://tooltranslate.toolforge.org/#tool=" + me.toolinfo.meta.id + "' target='_blank' style='text-decoration:none;font-size:2rem;vertical-align:middle;'>&#x1f30d;</a>";
            h += "</form>";
            $(target).html(h);
            $(target).find('select').change(function () {
                var o = $(this);
                var lang = o.val();
                me.setLanguage(lang);
                if (typeof me.onLanguageChange != 'undefined') me.onLanguageChange(lang);
            });
        }

        if (typeof me.language_cache == 'undefined') {
            $.get(me.tool_path + 'data/languages.json', function (d) {
                me.language_cache = d;
                me.language_cache["ar"] = "العربية";
                addDropdown();
            }, 'json');
        } else {
            addDropdown();
        }
    }

    // CONSTRUCTOR
    var to_load = [];
    var language_from_cookie = this.getCookie('interface_language');
    if (typeof intitial_params.language !== 'undefined' && intitial_params.language != '' && intitial_params.language != null) {
        this.language = intitial_params.language;
        if (intitial_params.language != 'en') to_load.push(intitial_params.language);
    } else if (language_from_cookie != '') {
        this.language = language_from_cookie;
        if (language_from_cookie != 'en') to_load.push(language_from_cookie);
    }
    if (typeof intitial_params.languages != 'undefined') {
        $.each(intitial_params.languages, function (k, v) {
            if (v == 'en' || -1 != $.inArray(v, to_load)) return;
            to_load.push(v);
        });
    }
    to_load.push('en');
    if (-1 == $.inArray(this.language, to_load)) to_load.push(this.language);
    this.loadToolTranslation(to_load, intitial_params.callback);
}
