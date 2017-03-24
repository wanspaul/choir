from django.http import HttpResponseRedirect


def root(request):
    """
    루트 경로로 접근시 리다이렉트
    :param request:
    :return:
    """
    redirect_url = '/attendance/home/'
    return HttpResponseRedirect(redirect_url)
