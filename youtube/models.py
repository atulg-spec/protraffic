from django.db import models, transaction
from django.contrib.auth.models import User


class EmailAccounts(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=255, default="")
    tag = models.CharField(max_length=255, default="")
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Email Account"
        verbose_name_plural = "Email Accounts"

class EmailAccountDataUpload(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    data = models.TextField(default="")
    tag = models.CharField(max_length=30, default="")

    class Meta:
        verbose_name = "Email Account Data"
        verbose_name_plural = "Upload Accounts"

    def __str__(self):
        return f"Email Data Uploaded"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Split the data field into individual email addresses and passwords
        lines = self.data.splitlines()
        for i in range(0, len(lines), 2):  # Process every two lines (email and password)
            email = lines[i].strip()
            password = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if email:  # Check if the email is not empty
                # Create or update EmailAccounts entry for each email
                email_account, created = EmailAccounts.objects.get_or_create(
                    user=self.user,
                    email=email,
                    defaults={'password': password, 'tag': self.tag}
                )
                if not created:
                    email_account.password = password
                    email_account.tag = self.tag
                    email_account.save()
