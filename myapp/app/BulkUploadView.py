
from flask_appbuilder import SimpleFormView, expose
from flask import flash, request, redirect
from flask_appbuilder.forms import DynamicForm
from wtforms import FileField
from flask_wtf.file import FileRequired
from werkzeug.utils import secure_filename
import csv
import os

from . import appbuilder, db
from .models import BareMetal


class BulkUploadForm(DynamicForm):
    file = FileField(label='Upload CSV', validators=[FileRequired()])


class BulkUploadView(SimpleFormView):
    form = BulkUploadForm
    form_title = 'Bulk Upload BareMetals'
    form_template = 'bulk_upload.html'


    @expose('/', methods=['GET', 'POST'])
    def index(self):
        self.update_redirect()

        # 生成或刷新表单实例
        form = self.form.refresh() if hasattr(self.form, 'refresh') else self.form()

        if request.method == 'POST':
            if form.validate_on_submit():
                # 文件上传和表单验证成功的处理...
                flash('Successfully uploaded and processed.', 'success')
            else:
                # 表单验证失败
                flash('Form validation failed.', 'error')

        # 注意这里我们总是传递 form 给模板
        return self.render_template(self.form_template,
                                    form=form,
                                    appbuilder=self.appbuilder)

    @expose('/', methods=['GET'])
    def this_form_get(self):
        self.update_redirect()
        form = self.form.refresh() if hasattr(self.form, 'refresh') else self.form()
        return self.render_template(self.form_template,
                                    title=self.form_title,
                                    form=form,
                                    appbuilder=self.appbuilder)

    @expose('/', methods=['POST'])
    def this_form_post(self):
        form = self.form.refresh() if hasattr(self.form, 'refresh') else self.form()
        if form.validate_on_submit():
            try:
                uploaded_file = form.file.data
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(appbuilder.app.config['UPLOAD_FOLDER'], filename)
                uploaded_file.save(file_path)

                with open(file_path, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    header = next(reader)  # Expecting a header row in CSV file
                    for row in reader:
                        new_machine = BareMetal(sn=row[0], ip=row[1], bmcip=row[2], adress=row[3])
                        db.session.add(new_machine)
                    db.session.commit()
                flash('Successfully uploaded and inserted records.', 'info')
            except Exception as e:
                flash('Failed to upload and insert records. Error: {}'.format(str(e)), 'danger')

            return redirect(self.get_redirect())  # Redirect after POST
        else:
            return self.render_template(self.form_template,
                                        title=self.form_title,
                                        form=form,
                                        appbuilder=self.appbuilder)



# # 添加BulkUploadView到侧边栏菜单中
# appbuilder.add_link(
#     "Bulk Upload",
#     href='/bulkuploadview/',
#     category='Data Management',
#     category_icon="fa-database"
# )
appbuilder.add_view(
    BulkUploadView,
    "Bulk Upload BareMetals",
    icon="fa-upload",
    category="Data Management",
    category_icon="fa-database"
)