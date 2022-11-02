from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Posts'
class UsersConfig(AppConfig):
    name= 'users'

    def ready(self):
        import Posts.signals


