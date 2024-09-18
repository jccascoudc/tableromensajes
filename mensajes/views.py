from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from mensajes.models import Mensaje
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

class RegistroUsuario(CreateView):
    template_name = 'registration/registro.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


def home_view(request):
    return render(request,'home.html')

class CrearMensaje(LoginRequiredMixin, CreateView):
    model = Mensaje
    fields = ['destinatario', 'contenido']
    template_name = 'enviar_mensaje.html'
    success_url = reverse_lazy('mensajes_recibidos')

    def form_valid(self, form):
        form.instance.remitente = self.request.user
        return super().form_valid(form)


class MensajesRecibidos(LoginRequiredMixin, ListView):
    model = Mensaje
    template_name = 'mensajes_recibidos.html'

    def get_queryset(self):
        return Mensaje.objects.filter(destinatario=self.request.user)
    

class EliminarMensaje(LoginRequiredMixin, DeleteView):
    model = Mensaje
    template_name = 'confirmar_eliminacion.html'
    success_url = reverse_lazy('mensajes_recibidos')

    def get_queryset(self):
        return Mensaje.objects.filter(destinatario=self.request.user)


class EditarMensaje(LoginRequiredMixin,UpdateView):
    model = Mensaje
    template_name = 'editar_mensaje.html'
    fields = ['destinatario','contenido']
    success_url = reverse_lazy('mensajes_recibidos')