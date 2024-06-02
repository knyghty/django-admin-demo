from django.shortcuts import redirect


def redirect_to_admin(request):
    return redirect("admin:index")
