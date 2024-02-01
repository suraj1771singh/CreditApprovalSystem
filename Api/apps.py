from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Api'
    def ready(self) :
        from .tasks import import_excel_data
        import_excel_data.delay()
        return super().ready()
