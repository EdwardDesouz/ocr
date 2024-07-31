import os
import ocrmypdf
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            output_path = os.path.join(settings.MEDIA_ROOT, f"ocr_{filename}")

            try:
                ocrmypdf.ocr(file_path, output_path, skip_text=True)
                return render(request, 'ocrapp/download.html', {'filename': f"ocr_{filename}"})
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}")

    else:
        form = UploadFileForm()
    return render(request, 'ocrapp/upload.html', {'form': form})

def download_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    return HttpResponse("File does not exist.")
