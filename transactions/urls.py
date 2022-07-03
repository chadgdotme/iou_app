from django.urls import path
from . import views

app_name = "transactions"

urlpatterns = [
    path(
        "transactions/add/",
        views.TransactionCreateView.as_view(),
        name="add_transaction",
    ),
    path("transactions/search/", views.SearchListView.as_view(), name="search"),
    path(
        "transactions/<int:pk>/",
        views.TransactionDetailView.as_view(),
        name="transaction_details",
    ),
    path(
        "transactions/<int:pk>/delete/",
        views.TransactionDeleteView.as_view(),
        name="delete_transaction",
    ),
    path("", views.TransactionListView.as_view(), name="index"),
]
