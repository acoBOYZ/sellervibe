from django.contrib.auth import get_user_model
CustomUser = get_user_model()

def create_user_with_profile_picture(strategy, details, backend, user=None, response=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    email = details.get('email')
    username = details.get('username') or details.get('email').split('@')[0]
    first_name = details.get('first_name')
    last_name = details.get('last_name')
    profile_picture_url = response.get('picture')
    provider = backend.name

    if backend.name == 'google-oauth2':
        try:
            user = CustomUser.objects.get(email=email)
            return {'is_new': False}
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(username=username, email=email, password=None, first_name=first_name, last_name=last_name, profile_picture_url=profile_picture_url, provider=provider)
        except CustomUser.MultipleObjectsReturned:
            user = CustomUser.objects.filter(email=email).order_by('id').first()
        user.save()

    return {'is_new': True, 'user': user}