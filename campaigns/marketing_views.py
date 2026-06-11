from django.shortcuts import render


def home(request):
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect("dashboard")
    return render(request, "marketing/home.html")


def features(request):
    return render(request, "marketing/features.html")


def pricing(request):
    return render(request, "marketing/pricing.html")


def download(request):
    return render(request, "marketing/download.html")
