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

        # TODO: Move legend data to a model
        chart_legend = [
        {"color": "yellow", "text": "Human Rights Violations"},
        {"color": "jade", "text": "Environmental Harm"},
        {"color": "raspberry", "text": "Animal Cruelty"},
        {"color": "brown", "text": "Weapons"},
        {"color": "purple", "text": "Fossil Fuels"},
        {"color": "violet", "text": "Social Harm"},
        ]
        context["chart_legend"] = chart_legend
        return context
