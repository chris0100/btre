from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']
        user_id = request.POST['listing_id']
        realtor_email = request.POST['realtor_email']

        #revisar si el usuario ha hecho ya un inquiry
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)

            if has_contacted:
                messages.error(request, 'Ud ya ha hecho un Inquiry para este item')
                return redirect('/listings/' + listing_id)


        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

        contact.save()

        # Enviar email
        send_mail(
            'Property Listing Inquiry',
            'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
            'alexroguez59@gmail.com',
            #a quienes se envia el correo, al vendedor y al usuario
            [realtor_email, email],
            fail_silently=False
        )

        messages.success(request,'Su solicitud ha sido enviada, alguien se comunicara con ud')

        return redirect('/listings/'+listing_id)



