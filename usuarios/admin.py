# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm, Select, TextInput, NumberInput

from .models import administradores
from prendas.models import clientes
from django.conf import settings

#MIRAR PARA QUE ES L CAMPO ES_SUPERUSER Y TRMINAR ESTA VAINA

# Register your models here.
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = administradores
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
        
    password = ReadOnlyPasswordHashField(label= ("Contraseña"))

    class Meta:
        model = administradores
        fields = ('username', 'email', 'password', 'is_active',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserChangeForm, self).save(commit=False)
        user.save()
        return user

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UsuarioAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'Nombre_apellido', 'cedula','seeGroups','is_active')
    list_filter = ('groups','genero')
    suit_list_filter_horizontal = ('groups','genero')
    readonly_fields = ['cambiar_contrasenia',]

    def seeGroups(self, obj):
        if obj.groups.all().count() > 0:
            roles = ""
            for group in obj.groups.all():
                roles += str(group.name) + ", "
            return roles
        else:
            return " - "
    seeGroups.short_description = "Roles"

    fieldsets = (
        ("Información Personal", 
            {'fields': ('cedula','clientes_fk','first_name', 'last_name', 'genero' ,'email', 'direccion', 'telefono')}
        ),

        ("Cuenta", 
            {'fields': ('username', 'password','cambiar_contrasenia')}
        ),
        ("Administrar Permisos", 
            {'fields': ('user_permissions', 'groups', 'is_active', 'is_staff', 'is_superuser',)}
        ),
        ("Fechas de acceso", {'fields': ('last_login', 
                        'date_joined',)}),
        
    )

    search_fields = ('first_name', 'last_name','cedula',)
    ordering = ('email',)
    #filter_horizontal = ('user_permissions','groups',)


    ''' def get_readonly_fields(self, request, obj=None):
    # make all fields readonly
        readonly_fields = ['cambiar_contrasenia',]
        if request.user.is_superuser==False:
            if (request.user.es_superuser==True):
                readonly_fields = ['user_permissions','is_superuser','last_login','date_joined','cambiar_contrasenia','fecha_limite',]
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
            else:
                readonly_fields = ['user_permissions','groups','is_active','is_staff','is_superuser','im_cliente_id','last_login','date_joined','es_superuser','cambiar_contrasenia','fecha_limite']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
            return readonly_fields
        return readonly_fields '''

    """ def get_queryset(self, request):
        qs = super(UsuarioAdmin, self).get_queryset(request)
        if len(request.user.groups.all()) > 0:
            ''' if (request.user.es_superuser==True):
                if request.user.groups.all()[0].name in settings.GROUP_PERMI:
                    used= qs.filter(im_cliente_id__pk = request.user.im_cliente_id.pk)
                else:
                    used = qs.filter(pk=0)
                return used '''
            if request.user.groups.all()[0].name in settings.GROUP_PERMI:
                try:
                    used= qs.filter(pk = request.user.pk)
                except:
                    used= qs.filter(pk =0)
            else:
                used=qs.filter(pk =0)
            return used
        elif request.user.is_superuser:
            return qs """

    ''' def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if (not request.user.is_superuser):
            if db_field.name == 'im_cliente_id':
               kwargs["queryset"] = im_cliente.objects.filter(pk=request.user.im_cliente_id.pk)
            else:
                pass
        return super(UsuarioAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs) '''

admin.site.register(administradores, UsuarioAdmin)

