from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Making my custom create user
    """

    def create_user(self, email, password, first_name, last_name, sex, D_O_B):

        if not email:
            raise ValueError(_('The Email must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, sex=sex, D_O_B=D_O_B)
        user.set_password(password)
        user.save()
        return user

    def add_profile_pic(self, user, profile_pic):
        pic = self.model(user_id=user, profile_pic=profile_pic)
        pic.save()

        return pic