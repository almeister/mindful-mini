from django.views import generic

from .models import Category, Fund


class IndexView(generic.ListView):
    template_name = "kiwisaver/index.html"
    context_object_name = "fund_list"

    def get_queryset(self):
        return Fund.objects.order_by("name")


class DetailView(generic.DetailView):
    model = Fund
    template_name = "kiwisaver/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
