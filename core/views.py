from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactMessageForm


def home(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
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
            except Exception:
                messages.error(
                    request,
                    "Désolé, une erreur est survenue pendant l'envoi de l'email. Réessayez.",
                )
                return redirect(f"{reverse('home')}#contact")

            # Affiche le message de succès une seule fois (puis le supprime à l'actualisation)
            request.session["contact_sent"] = True
            request.session.modified = True
            return redirect(f"{reverse('home')}#contact")
        messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form = ContactMessageForm()

    sent = request.session.pop("contact_sent", False)
    return render(request, "core/home.html", {"form": form, "sent": sent})
