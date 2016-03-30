from django.shortcuts import render
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django import forms

from PIL import Image

import StringIO

class UploadImageForm(forms.Form):
  image = forms.ImageField()
  
def __pixelate__(image_file):
  image = Image.open(image_file)
  pixel_size = image.size[0] / 25
  image = image.resize((image.size[0]/pixel_size, image.size[1]/pixel_size), Image.NEAREST)
  image = image.resize((image.size[0]*pixel_size, image.size[1]*pixel_size), Image.NEAREST)

  image_out = StringIO.StringIO()
  image.save(image_out, 'PNG', compress_level=0)
  image_out.seek(0)

  return image_out

def pixelate_photo(request):
  if request.method == 'POST':
    form = UploadImageForm(request.POST, request.FILES)
    if form.is_valid():
      input_img = request.FILES['image']
      input_filename = input_img.name
      pixelated_img = __pixelate__(input_img)
      resp = HttpResponse(content_type = 'image/jpeg')
      resp['Content-Disposition'] = 'attachment; filename=%s.png' % input_filename[:input_filename.rfind('.')]
      resp.write(pixelated_img.getvalue())
      return resp

  else:
    form = UploadImageForm()
  return render(request, 'upload.html', {'form': form})

