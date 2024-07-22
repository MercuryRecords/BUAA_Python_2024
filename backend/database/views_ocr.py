import os
import shutil
import fitz
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from paddleocr import PaddleOCR

img_formats = ["jpeg", "jpg", "png", "tiff", "tif", "bmp"]


def pdf_to_images(pdf_path, output_folder):
    os.mkdir(output_folder)
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc[page_num]
        pix = page.get_pixmap()
        pix.save(f"{output_folder}/page_{page_num}.png")


@require_http_methods(["POST"])
def pdf_text(request):
    upload_file = request.FILES['file']
    if upload_file.name.split('.')[-1] == 'pdf':
        text = []
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'upload/pdf'))
        filename = fs.save(upload_file.name, upload_file)
        uploaded_file_path = fs.path(filename)
        output_folder = os.path.join(settings.MEDIA_ROOT, f'upload/pdf/{filename.split(".")[0]}')
        pdf_to_images(uploaded_file_path, output_folder)
        ocr = PaddleOCR(lang="ch", use_angle_cls=True, use_gpu=True)
        for page_img in os.listdir(output_folder):
            page_img_path = os.path.join(output_folder, page_img)
            result = ocr.ocr(page_img_path)
            if result and result[0]:
                text += [line[1][0] for line in result[0]]

        os.remove(uploaded_file_path)
        shutil.rmtree(output_folder)

        return JsonResponse({"code": 200, 'text': text})

    elif upload_file.name.split('.')[-1] in img_formats:
        text = []
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'upload/img'))
        filename = fs.save(upload_file.name, upload_file)
        uploaded_file_path = fs.path(filename)
        ocr = PaddleOCR(lang="ch", use_angle_cls=True, use_gpu=True)
        result = ocr.ocr(uploaded_file_path)

        for line in result[0]:
            text.append(line[1][0])

        os.remove(uploaded_file_path)

        return JsonResponse({"code": 200, 'text': text})

    return JsonResponse({"code": 400, 'text': '上传文件格式错误'})
