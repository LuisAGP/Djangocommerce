from .models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Profile, ValidateEmail
from django.core.mail import send_mail

# When a new User is saved then run this function
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        validate = ValidateEmail.objects.create(user=instance, email=instance.email)
        send_mail(
            subject="Validación de correo para Djcommerce",
            message=f"Da click en el siguiente enlace para validar tu correo http://localhost:8000/validate/{validate.id}",
            from_email="angel.lagp98@gmail.com",
            recipient_list=[validate.user.email]
        )




@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, *args, **kwargs):
    
    try:
        instance.photo.delete(save=False)
    except:
        pass



@receiver(pre_save, sender=Profile)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).photo.path
        try:
            new_img = instance.photo.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass