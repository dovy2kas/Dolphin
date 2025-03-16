from django.db import models

class Client(models.Model):
    mac = models.CharField(max_length=17, unique=True, null=True)
    status = models.CharField(max_length=20, default='offline')
    last_seen = models.DateTimeField(auto_now=True)
    os = models.CharField(max_length=50, blank=True, null=True)
    arch = models.CharField(max_length=10, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    privileges = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.mac

class Command(models.Model):
    bot = models.ForeignKey(Client, on_delete=models.CASCADE)
    command = models.CharField(max_length=256, null=True)
    payload_url = models.URLField(blank=True, null=True)
    args = models.TextField(blank=True, null=True)
    executed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bot.mac} -> {self.command}"

class Payload(models.Model):
    os = models.CharField(max_length=50)
    format = models.CharField(max_length=50)
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.os} - {self.format} - {self.file_path}"
