from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # This sends a signal to those apps that are listening. 
    def ready(self) -> None:
        import r2p.signals
        return super().ready()