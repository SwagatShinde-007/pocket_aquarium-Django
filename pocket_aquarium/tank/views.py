import random

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import FishForm
from .models import Fish


def index(request):
    if request.method == "POST":
        form = FishForm(request.POST)
        if form.is_valid():
            fish = form.save(commit=False)
            fish.depth = random.randint(16, 76)
            fish.save()
            return redirect(f"{reverse('tank:index')}?new={fish.pk}")
    else:
        form = FishForm(initial={"color": "#ff6f59", "size": 110, "speed": 16})

    fish_list = Fish.objects.all()
    total_meals = fish_list.aggregate(total=Sum("meals"))["total"] or 0
    return render(
        request,
        "tank/index.html",
        {"fish_list": fish_list, "form": form, "total_meals": total_meals},
    )


@require_POST
def feed(request, pk):
    fish = get_object_or_404(Fish, pk=pk)
    fish.meals += 1
    fish.save(update_fields=["meals"])
    return JsonResponse(
        {"meals": fish.meals, "size": fish.display_size, "level": fish.level}
    )


@require_POST
def release(request, pk):
    get_object_or_404(Fish, pk=pk).delete()
    return JsonResponse({"ok": True})
