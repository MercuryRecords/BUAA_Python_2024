import os
import fitz
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def pdf_text(request):
    pdf_file = request.FILES['file']
    
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'upload/pdf'))
    filename = fs.save(pdf_file.name, pdf_file)
    uploaded_file_path = fs.path(filename)

    # print(uploaded_file_path)

    doc = fitz.open(uploaded_file_path)
    
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    return JsonResponse({"code": 200, 'text': text})
