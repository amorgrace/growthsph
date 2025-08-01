# apiconf/email.py
# from djoser.email import ActivationEmail
# from djoser import email

# class CustomActivationEmail(ActivationEmail):
#     template_name = "email/activation.txt"

#     def get_context_data(self):
#         context = super().get_context_data()
#         context["domain"] = "growthsph.com"
#         context["site_name"] = "Growthsph"
#         context["protocol"] = "http"  # Use "http" for local, "https" for production
#         context["activation_url"] = self.get_activation_url(context)
#         return context
# apiconf/email.py

from djoser.email import ActivationEmail

class CustomActivationEmail(ActivationEmail):
    template_name = "email/activation.txt"

    def get_context_data(self):
        context = super().get_context_data()
        uid = context.get("uid")
        token = context.get("token")
        # domain = context.get("domain")
        # protocol = context.get("protocol")

        # context["activation_url"] = f"http://localhost:5173/activate/{uid}/{token}/"
        context["activation_url"] = f"http://growthsph.com/activate/{uid}/{token}/"

        return context
