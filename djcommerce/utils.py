from django.http import HttpResponse
import sys, os
import json


def json_response(response):
    return HttpResponse(json.dumps(response, indent=4, sort_keys=True, default=str), content_type="application/json")


def get_error_info(error):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return exc_type, fname, exc_tb.tb_lineno