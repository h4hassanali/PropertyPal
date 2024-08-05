from django.db import models

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
    image = models.ImageField(upload_to='room_images/')
    info = models.TextField()
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=100)  # Added default value
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listed_rooms')

    def __str__(self):
        return f"Room in {self.city.city_name} listed by {self.listed_by.username}"

class RoommateProfile(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='roommate_profiles')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='roommate_profile')
    contact_info = models.CharField(max_length=100)
    image = models.ImageField(upload_to='roommate_images/', blank=True, null=True)  # Added image field
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Added budget attribute

    def __str__(self):
        return f"{self.user.username} in {self.city.city_name}"

class Accessory(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='accessories')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accessories')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='accessory_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Added price attribute

    def __str__(self):
        return f"{self.name} in {self.city.city_name}"
