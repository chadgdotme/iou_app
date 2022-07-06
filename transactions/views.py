from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic, View
from .forms import TransactionForm
from .models import Transaction

# Create your views here.


class Helper:
    def calculate_balance(self):
        total = 0
        for transaction in Transaction.objects.all():
            if transaction.type == "CR":
                total += transaction.amount
            else:
                total -= transaction.amount
        return total


class TransactionListView(generic.ListView, Helper):
    model = Transaction
    ordering = ("-date",)
    template_name = "index.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["balance"] = self.calculate_balance()
        return context


class TransactionDetailGetView(generic.DetailView, Helper):
    model = Transaction
    template_name = "transaction_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["balance"] = self.calculate_balance()
        context["form"] = TransactionForm(instance=self.get_object())
        return context


class TransactionDetailPostView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
    Helper,
):
    model = Transaction
    fields = ("date", "description", "type", "amount", "notes")
    template_name = "transaction_details.html"
    success_url = reverse_lazy("transactions:index")
    success_message = "Transaction updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["balance"] = self.calculate_balance()
        return context

    def test_func(self):
        transaction = self.get_object()
        return transaction.user == self.request.user


class TransactionDetailView(View):
    def get(self, request, *args, **kwargs):
        view = TransactionDetailGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TransactionDetailPostView.as_view()
        return view(request, *args, **kwargs)


class TransactionCreateView(
    LoginRequiredMixin, SuccessMessageMixin, generic.CreateView, Helper
):
    model = Transaction
    form_class = TransactionForm
    template_name = "add_transaction.html"
    success_url = reverse_lazy("transactions:index")
    success_message = "Transaction added successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user  # type: ignore
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["balance"] = self.calculate_balance()
        return context


class TransactionDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    generic.DeleteView,
    Helper,
):
    model = Transaction
    template_name = "delete_transaction.html"
    success_url = reverse_lazy("transactions:index")
    success_message = "Transaction deleted successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["balance"] = self.calculate_balance()
        context["form"] = TransactionForm(instance=self.get_object())
        return context

    def test_func(self):
        transaction = self.get_object()
        return transaction.user == self.request.user


class SearchListView(generic.ListView, Helper):
    model = Transaction
    template_name = "search.html"
    context_object_name = "transactions"
    paginate_by = 20

    def get_queryset(self):
        search = self.request.GET.get("q")
        return (
            Transaction.objects.filter(description__icontains=search).order_by("-date")
            if search
            else Transaction.objects.none()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["balance"] = self.calculate_balance()
        search = self.request.GET.get("q")
        context["search"] = search
        context["count"] = (
            Transaction.objects.filter(description__icontains=search).count()
            if search
            else 0
        )
        return context
