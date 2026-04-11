from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
import logging

from .forms import ContactMessageForm

logger = logging.getLogger(__name__)


def home(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Essayer d'envoyer l'email, mais ne pas bloquer le formulaire si ça échoue
            try:
                send_mail(
                    subject=f"Nouveau message portfolio: {contact_message.subject}",
                    message=(
                        f"Nom: {contact_message.name}\n"
                        f"Email: {contact_message.email}\n\n"
                        f"Message:\n{contact_message.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    "Merci ! Votre message a été reçu et un email a été envoyé."
                )
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi d'email: {str(e)}")
                messages.warning(
                    request,
                    "Votre message a été reçu, mais une erreur s'est produite lors de l'envoi de l'email. Nous l'avons noté."
                )
            
            # Affiche le message de succès une seule fois (puis le supprime à l'actualisation)
            request.session["contact_sent"] = True
            request.session.modified = True
            return redirect(f"{reverse('home')}#contact")
        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form = ContactMessageForm()

    sent = request.session.pop("contact_sent", False)
    return render(request, "core/home.html", {"form": form, "sent": sent})
