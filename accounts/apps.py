from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    # def ready(self):  # method just to import the signals
    #     import django.db.models.signals
