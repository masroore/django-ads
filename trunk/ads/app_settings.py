from django.conf import settings

PROJECT_ROOT_URL = getattr(settings, 'PROJECT_ROOT_URL', None)

ADS_UPLOAD_CSS_PATH = getattr(settings, 'ADS_UPLOAD_CSS_PATH', None)
ADS_MEDIA_URL = getattr(settings, 'ADS_MEDIA_URL', settings.MEDIA_URL+'ads/')
ADS_ROOT_URL = getattr(settings, 'ADS_ROOT_URL', PROJECT_ROOT_URL+'ads/')
ADS_SYSTEM_MARK = getattr(settings, 'ADS_SYSTEM_MARK', 'WN Advertising System')

ADS_CHARTS_WIDTH = getattr(settings, 'ADS_CHARTS_WIDTH', "80%")
ADS_CHARTS_HEIGHT = getattr(settings, 'ADS_CHARTS_HEIGHT', 200)

ADS_STORED_META_KEYS = ('LANG','HTTP_USER_AGENT','HTTP_CONNECTION','REMOTE_ADDR',
        'REMOTE_HOST','HTTP_ACCEPT_ENCODING','HTTP_ACCEPT_LANGUAGE','COUNTRY_CODE',
        'GMT_DIFF')
