from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Votre nom",
                    "class": "w-full bg-sky-950 border border-cyan-700 text-sky-50 rounded-lg px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-cyan-500/30 focus:border-cyan-400",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "vous@email.com",
                    "class": "w-full bg-sky-950 border border-cyan-700 text-sky-50 rounded-lg px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-cyan-500/30 focus:border-cyan-400",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "placeholder": "Sujet",
                    "class": "w-full bg-sky-950 border border-cyan-700 text-sky-50 rounded-lg px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-cyan-500/30 focus:border-cyan-400",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Votre message",
                    "rows": 6,
                    "class": "w-full bg-sky-950 border border-cyan-700 text-sky-50 rounded-lg px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-cyan-500/30 focus:border-cyan-400",
                }
            ),
        }
