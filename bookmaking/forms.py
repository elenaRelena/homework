from django import forms
from .models import User1, Horse, Stake, Ride
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import pymysql
pymysql.install_as_MySQLdb()


class RegForm(forms.Form):
    username1 = forms.CharField(label='Пользователь', min_length=5)
    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', min_length=8, widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', min_length=1)
    surname = forms.CharField(label='Фамилия', min_length=1)
    name = forms.CharField(label='Имя', min_length=1)

    def clean(self):
        value = super(RegForm, self).clean()
        password = value.get('password')
        password2 = value.get('password2')
        if password != password2:
            raise forms.ValidationError('Пароли должны совпадать')
        users = User.objects.filter(username=value.get('username1'))
        if len(users) > 0:
            raise forms.ValidationError('Пользователь с таким именем уже существует')


class LoginForm(forms.Form):
    username1 = forms.CharField(label='Username', min_length=5)
    password = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if not self.errors:
            user = authenticate(username=cleaned_data['username1'], password=cleaned_data['password'])
            if user is None:
                raise forms.ValidationError('Неверный логин или пароль')
            self.user = user
        return cleaned_data

    def get_user(self):
        return self.user or None


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean(self):
        value = super(UserForm, self).clean()
        if len(value.get('first_name')) == 0:
            raise forms.ValidationError('Поле Имя должно быть заполнено')
        if len(value.get('last_name')) == 0:
            raise forms.ValidationError('Поле Фамилия должно быть заполнено')
        if len(value.get('email')) == 0:
            raise forms.ValidationError('Поле Email должно быть заполнено')


class User1Form(forms.ModelForm):
    class Meta:
        model = User1
        fields = ('age', 'bank_account', 'contacts', 'avatar')

    def clean(self):
        value = super(User1Form, self).clean()
        if len(value.get('bank_account')) == 0:
            raise forms.ValidationError('Поле Банковский аккаунт должно быть заполнено')
        if len(value.get('contacts')) == 0:
            raise forms.ValidationError('Поле Контакты должно быть заполнено')

            # def save(self, pk, commit):
            #     us = User1()
            #     us.age = self.cleaned_data.get('age')
            #     us.bank_account = self.cleaned_data.get('bank_account')
            #     us.contacts = self.cleaned_data.get('contacts')
            #     us.user = pk
            #     p = self.cleaned_data.get('avatar')
            #     file_url = r'/media/%s%s' % (us.contacts, '.jpg')
            #     filename = FileSystemStorage().save('/home/helen/PycharmProjects/lab6/bookmaking' + file_url, File(p))
            #     us.avatar = file_url
            #     us.save()


class MakeStake(forms.ModelForm):
    class Meta:
        model = Stake
        fields = ('size', 'horse')

    def __unicode__(self):
        return self.horse.name

    def __str__(self):
        return self.horse.name
        # def clean(self, request):
        #     value = super(MakeStake, self).clean()
        #     horses = Stake.objects.filter(horse=value.get('horse'), user = request.user.id)
        #     if len(horses) > 0:
        #         raise forms.ValidationError('Вы уже поставили на эту лошадь')


class HorseForm(forms.ModelForm):
    class Meta:
        model = Horse
        fields = ('name',)


class MakeStake1(forms.Form):
    horse_name = forms.CharField(label='Лошадь')
    stake_size = forms.FloatField(label='Ставка')

    def clean(self):
        value = super(MakeStake1, self).clean()
        horse_name = value.get('horse_name')
        stake_size = value.get('stake_size')
        horses = Horse.objects.filter(name=value.get('horse_name'))
        if len(horses) == 0:
            raise forms.ValidationError('Такой лошади не существует')
