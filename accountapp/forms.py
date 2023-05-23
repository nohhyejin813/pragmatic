from django.contrib.auth.forms import UserCreationForm

class AccountUpdateForm(UserCreationForm):
    def __int__(self, *args, **kwargs):
        super().__int__(*args, **kwargs)

        self.fields['username'].disabled = True