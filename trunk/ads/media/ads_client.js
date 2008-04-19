// django-ads client javascript
// Created by Marinho Brandao, 2008-04-17
// http://code.google.com/p/django-ads/

// Continues only if adbox variable is valid
if (cont_id != undefined && website_id != undefined && adbox_id != undefined) {
    var ADS_SERVER_URL = 'http://localhost:8000/';

    //-----------------------
    // DOES NOT CHANGE BELOW
    //-----------------------

    var ADS_SERVER_GET_ADS_URL = ADS_SERVER_URL+'ads/website/'+website_id+'/adbox/'+adbox_id+'/get_ads/';
    var MAX_WORDS = 100;
    var INVALID_WORDS = ['this','the']
    var collected_words = [];

    letters_count = function(txt) {
        var ret = 0;
        
        for (var i=0; i<txt.length; i++) {
            var c = txt.charCodeAt(i);
            ret += (c >= 65 && c <= 90) || (c >= 97 && c <= 122) ? 1 : 0 ;
        }

        return ret;
    }

    get_words = function(txt){
        var words = txt.split(' ');

        for (var i=0; i<words.length; i++) {
            w = words[i].toLowerCase();

            if (letters_count(w) >= 3 && collected_words.indexOf(w) == -1 && INVALID_WORDS.indexOf(w) == -1) {
                collected_words.push(w);
            }
        }
    }

    // Parses document for relevant words
    $('title, h1, h2, h3, h4').each(function(){ get_words($(this).text()); });
    $('meta[name=keywords], meta[name=description]').each(function(){ get_words(this.content); });

    var collected_words = collected_words.length <= MAX_WORDS ? collected_words : collected_words.slice(0,MAX_WORDS);

    // Referer URL
    var ref = window.location.href;

    // Remove arguments
    if (ref.indexOf('?')) ref = ref.split('?')[0]
    if (ref.indexOf('#')) ref = ref.split('#')[0]

    // Generate iframe with its properties
    $('#'+cont_id).before('<iframe id="'+cont_id+'_f" src="'+ADS_SERVER_GET_ADS_URL+'?referer='+ref+'&words='+collected_words+'"/>');
    $('#'+cont_id).remove();

    $('#'+cont_id+'_f').css('height', adbox_height+'px');
    $('#'+cont_id+'_f').css('width', adbox_width+'px');
    $('#'+cont_id+'_f').css('border', 'none');
    $('#'+cont_id+'_f').css('overflow', 'hidden');
}

