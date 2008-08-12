"""
How to use it:

# SIGNALS AND LISTENERS
from django.dispatch import dispatcher
from apps.ads import app_signals as ads_signals

def get_meta_info(sender, meta):
    meta.update({'COUNTRY_CODE':'BR', 'GMT_DIFF':-3})

dispatcher.connect(get_meta_info, signal=ads_signals.get_meta_info)
"""
try:
    from django.dispatch import Signal
    get_meta_info = Signal()
except ImportError:
    get_meta_info = object()

