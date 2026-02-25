from django.http import HttpResponse


def test_view(request):
    return HttpResponse("<h1>DDDDjangodan salomlar</h1>")