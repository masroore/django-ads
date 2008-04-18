// django-ads client javascript
// Created by Marinho Brandao, 2008-04-17
// http://code.google.com/p/django-ads/

// Continues only if adbox variable is valid
if (cont_id != undefined && website_id != undefined && adbox_id != undefined) {
    // Initialization
    var ADS_SERVER_URL = 'http://localhost:8000/';
    var ADS_SERVER_GET_ADS_URL = ADS_SERVER_URL+'ads/website/'+website_id+'/adbox/'+adbox_id+'/get_ads/';
    var ADS_SYSTEM_MARK = 'WN Advertising System';

    $('#'+cont_id).before('<link rel="stylesheet" href="'+ADS_SERVER_URL+'media/ads/ads_client.css"/>');
    $('#'+cont_id).attr('class', 'ads_ad');

    // Take first 50 in the content (featuring H1 and TITLE)
    var collected_words = '';

    // Data args
    var data = {
        words: collected_words,
    }

    // Sends ads requesting to server (URL, AdBox ID, collected words)
    $.getJSON(ADS_SERVER_GET_ADS_URL, data, function(json) {
        // Set CSS address
        $('#'+cont_id).before('<link rel="stylesheet" href="'+json['css']+'"/>');
    
        // Set dimensions to ads div
        //$('#'+cont_id).css('height', json['height']);
        //$('#'+cont_id).css('width', json['width']);

        // Receive response from Ads server
        var html = '<div class="ads_conteiner">';

        // Create Ads here
        for (var i=0; i<json['ads'].length; i++) {
            var ad = json['ads'][i];
            //var h = ad['height']-19;
            //var w = ad['width'];

            //html += '<div class="ads_ad" style="height: '+h+'px; width: '+w+'px">';
            html += '<div class="ads_ad">';
            html += '<a href="'+ad['url']+'">';
            html += '<h6>'+ad['title']+'</h6>';
            html += '<span class="ads_description">'+ad['description']+'</span>';
            html += '<span class="ads_url">'+ad['ad_url']+'</span>';
            html += '</a>';
            html += '</div>';
        }

        html += '</div>';
        html += '<div class="ads_footer">Ads by '+ADS_SYSTEM_MARK+'</div>';

        $('#'+cont_id).html(html);
    });
}

