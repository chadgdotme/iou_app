from django.contrib.auth import views
from transactions.views import Helper

# Create your views here.


class UserLoginView(views.LoginView, Helper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.extra_context = {
            "balance": self.calculate_balance(),
        }
        self.template_name = "login.html"
