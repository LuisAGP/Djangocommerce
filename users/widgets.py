from django.forms import widgets
from django.utils.safestring import mark_safe

class CustomPictureImageFieldWidget(widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        existing_HTML = super().render(name, value, attrs, **kwargs)
        img_html = f'''<div class="row">
                <div class="col-md-8 col-sm-12">
                    {existing_HTML}
                </div>
                <div class="col-md-4 col-sm-12">
                    <img src="{value.url}" width="200" class="img-fluid"/>
                </div>
            </div>'''
        return mark_safe(f'{img_html}')