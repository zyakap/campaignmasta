from django.contrib import messages
from django.shortcuts import redirect, render


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


def subscription_interest(request):
    from .forms import SubscriptionInterestForm

    form = SubscriptionInterestForm(request.POST or None)
    if form.is_valid():
        interest = form.save(commit=False)
        interest.created_by = request.user if request.user.is_authenticated else None
        interest.updated_by = request.user if request.user.is_authenticated else None
        interest.save()
        messages.success(request, "Thank you. Our team will contact you to confirm the appointment.")
        return redirect("marketing_subscription_interest")
    return render(request, "marketing/subscription_interest.html", {"form": form})
