# from django.dispatch import Signal, receiver
# from django.utils import autoreload
#
# RELOAD_SIGNAL = Signal()
#
#
# @receiver(signal=RELOAD_SIGNAL)
# def callback(**kwargs):
#     print("Restarting server...")
#     autoreload.restart_with_reloader()
# def restart_server(request):
#     restart.RELOAD_SIGNAL.send(sender="xxx")
#     return HttpResponse("")
# path('admin/restart', restart_server)
