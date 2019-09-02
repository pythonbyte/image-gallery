from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.views import View
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin, ListView

from .forms import PhotoForm
from .models import Photo

class ListPhotosView(FormView, MultipleObjectMixin):
    form_class = PhotoForm
    template_name = 'home_page.html'
    success_url = '/'
    paginate_by = 9

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super(ListPhotosView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        object_list = Photo.objects.filter(approved=True)
        order_param = self.request.GET.get('order')
        if order_param:
            object_list = object_list.order_by('-'+order_param)
        return super(ListPhotosView, self).get_context_data(object_list=object_list, **kwargs)


class ApprovePhotoListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Photo
    paginate_by = 6
    template_name = 'imageapp/approve-image.html'

    def get_queryset(self):
        return Photo.objects.filter(approved=False)


class ApprovePhotoView(LoginRequiredMixin, UpdateView):
    fields = ['approved']
    login_url = '/login'
    model = Photo
    success_url = '/approve-picture'

    def get_object(self):
        obj = Photo.objects.get(id=self.kwargs['id'])
        return obj

    def post(self, request, *args, **kwargs):
        try:
            photo = self.get_object()
            photo.approved = True
            photo.save()
            return super().post(request, *args, **kwargs)
        except Exception as exc:
            raise exc

class DeletePhotoView(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = Photo
    success_url = '/approve-picture'

    def get_object(self):
        obj = Photo.objects.get(id=self.kwargs['id'])
        return obj


class LikePhotoView(View):
    def post(self, request):
        if request.is_ajax():
            photo_id = request.POST.get('image_id')
            photo = Photo.objects.filter(id=photo_id).first()
            if photo:
                photo.likes += 1
                photo.save()
                json_data = {
                    "image": photo.id,
                    "likes": photo.likes
                }
                return JsonResponse(json_data, status=200)
            return JsonResponse({'error': 'Photo not found.'}, status=400)
        return JsonResponse({'error': 'Not allowed.'}, status=400)
