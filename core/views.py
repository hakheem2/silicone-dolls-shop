from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.contrib import messages
from order.models import Order
from cart.views import get_cart  # Assuming your cart logic

@require_POST
def submit_contact(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    message = request.POST.get("message")

    if not all([name, email, subject, message]):
        return JsonResponse({"success": False, "error": "All fields are required."})

    context = {
        'name': name,
        'email': email,
        'subject': subject,
        'message': message,
    }

    html_content = render_to_string('emails/contact_email.html', context)
    text_content = strip_tags(html_content)  # fallback for email clients that don't support HTML

    email_message = EmailMultiAlternatives(
        subject=f"[Contact] {subject}",
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['support@carolineheusssiliconedolls.com', 'hakheemwyatt2@gmail.com'],
    )
    email_message.attach_alternative(html_content, "text/html")

    try:
        email_message.send()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})



@require_POST
def submit_faq(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    question = request.POST.get("question")

    if not all([name, email, question]):
        return JsonResponse({"success": False, "error": "All fields are required."})

    context = {
        "name": name,
        "email": email,
        "question": question,
    }

    html_content = render_to_string("emails/faq_email.html", context)
    text_content = strip_tags(html_content)

    email_message = EmailMultiAlternatives(
        subject=f"[FAQ Question] from {name}",
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['support@carolineheusssiliconedolls.com', 'hakheemwyatt2@gmail.com'],
    )
    email_message.attach_alternative(html_content, "text/html")

    try:
        email_message.send()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

