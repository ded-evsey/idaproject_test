from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import ImageUploadForm, ImageChangeSize
from .models import Image
# Create your views here.


class ImageListView(ListView):
    model = Image
    template_name = 'images/list.html'


class ImageUploadView(CreateView):
    form_class = ImageUploadForm
    template_name = 'images/create.html'
    success_url = reverse_lazy('image_change')


class ImageChangeView(UpdateView):
    slug_field = 'pk'
    form_class = ImageChangeSize
    template_name = 'images/change.html'
    success_url = reverse_lazy('image_change')
    queryset = Image.objects.all()

    @staticmethod
    def get_size(request, instance):
        width = request.GET.get('width')
        height = request.GET.get('height')
        return (
            int(width if width else 0),
            int(height if height else 0)
        )

    def get_initial(self):
        initial = super().get_initial()
        initial['image_id'] = self.object.id
        size = self.get_size(self.request, self.object)
        initial['width'] = size[0]
        initial['height'] = size[1]
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['image'] = self.object.get_image(
            *self.get_size(self.request, self.object)
        )
        return context