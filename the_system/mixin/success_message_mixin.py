from django.contrib import messages
from django.forms.models import model_to_dict


class SuccessMessageMixin:
    """
    Add a success message on successful form submission.
    """
    success_message = ''
    activity_sender = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)


        if self.request.capture_user_activity:
                self.request.capture_user_activity.send(sender=self.get_activity_sender(), 
                                                    request=self.request, 
                                                    target=self.object,
                                                    message=success_message)    
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % model_to_dict(self.object)


    def get_activity_sender(self):
        return self.activity_sender or self.object.__class__.__name__