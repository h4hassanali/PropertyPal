from django.db import models
from django.utils.translation import gettext_lazy as _
class City(models.Model):
    city_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.city_name

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Consider using Django's built-in User model for better security.
    is_looking_for_room = models.BooleanField(default=False)
    is_looking_for_roommate = models.BooleanField(default=False)

    def __str__(self):
        return self.username
class Room(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='rooms')
    info = models.TextField()
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=100)  # Default value added
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listed_rooms')
    bills_included = models.BooleanField(default=False)  # Default value added
    for_female = models.BooleanField(default=False)  # Default value added
    adjusted_with_age_min = models.PositiveIntegerField(default=0)  # Default value added
    adjusted_with_age_max = models.PositiveIntegerField(default=100)  # Default value added
    room_size = models.CharField(max_length=10, choices=[('Single', 'Single'), ('Double', 'Double')], default='Single')  # Default value added
    num_of_rooms = models.PositiveIntegerField(default=1)  # Default value added
    smoking_allowed = models.BooleanField(default=False)  # Default value added
    length_of_stay_min = models.PositiveIntegerField(default=0)  # Default value added
    length_of_stay_max = models.PositiveIntegerField(default=12)  # Default value added
    move_on_timing = models.TimeField(null=True, blank=True)  # Default value added
    free_wifi = models.BooleanField(default=False)  # Default value added

    def __str__(self):
        return f"Room in {self.city.city_name} listed by {self.listed_by.username}"

class RoommateProfile(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='roommate_profiles')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='roommate_profile')
    contact_info = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    occupation = models.CharField(max_length=20, choices=[('Don\'t mind', 'Don\'t mind'), ('Professional', 'Professional'), ('Student', 'Student')], default='Don\'t mind')  # Default value added
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')  # Default value added
    music = models.CharField(max_length=20, choices=[('Occasionally', 'Occasionally'), ('Anytime', 'Anytime'), ('No', 'No')], default='Occasionally')  # Default value added
    smoking_allowed = models.BooleanField(default=False)  # Default value added
    timing_of_room_engagement = models.CharField(max_length=50, null=True, blank=True)  # Default value added
    adjusted_with_age_min = models.PositiveIntegerField(default=0)  # Default value added
    adjusted_with_age_max = models.PositiveIntegerField(default=100)  # Default value added
    bills_included = models.BooleanField(default=False)  # Default value added
    free_wifi = models.BooleanField(default=False)  # Default value added

    def __str__(self):
        return f"{self.user.username} in {self.city.city_name}"

class Accessory(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='accessories')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accessories')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} in {self.city.city_name}"
class Attachment(models.Model):
    class AttachmentType(models.TextChoices):
        PHOTO = "Photo", _("Photo")
        VIDEO = "Video", _("Video")

    file = models.FileField('Attachment', upload_to='attachments/')
    file_type = models.CharField('File type', choices=AttachmentType.choices, max_length=10)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    roommate_profile = models.ForeignKey(RoommateProfile, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)

    def clean(self):
        super().clean()
        if not self.file:
            raise ValidationError(_("No file uploaded."))
        
        if self.file_type == self.AttachmentType.PHOTO and not self.file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError(_("Invalid image format. Only PNG, JPG, JPEG are allowed."))
        elif self.file_type == self.AttachmentType.VIDEO and not self.file.name.lower().endswith(('.mp4', '.mov', '.avi')):
            raise ValidationError(_("Invalid video format. Only MP4, MOV, AVI are allowed."))

    def __str__(self):
        return f"{self.file_type} - {self.file.name}"

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'