// django-ads client javascript
// Created by Marinho Brandao, 2008-04-17
// http://code.google.com/p/django-ads/

// Continues only if adbox variable is valid
if (cont_id != undefined && website_id != undefined && adbox_id != undefined) {
    var ADS_SERVER_URL = 'http://localhost:8000/';
    var ADS_SERVER_GET_ADS_URL = ADS_SERVER_URL+'ads/website/'+website_id+'/adbox/'+adbox_id+'/get_ads/';

    $('#'+cont_id).before('<iframe id="'+cont_id+'_f" src="'+ADS_SERVER_GET_ADS_URL+'"/>');
    $('#'+cont_id).remove();

    $('#'+cont_id+'_f').css('height', adbox_height+'px');
    $('#'+cont_id+'_f').css('width', adbox_width+'px');
    $('#'+cont_id+'_f').css('border', 'none');
    $('#'+cont_id+'_f').css('overflow', 'hidden');
}

