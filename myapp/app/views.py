from datetime import datetime

from flask import render_template, request
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from flask_appbuilder.security.decorators import protect

from . import appbuilder,db
from .models import  BareMetal
from .security import check_jwt_token

from subprocess import run, PIPE, CalledProcessError

class BareMetalModelView(ModelView):
    datamodel = SQLAInterface(BareMetal)

    # 定义列表视图中显示哪些列
    list_columns = ['sn', 'ip', 'bmcip', 'adress','type','restart']

    # （可选）如果你想添加搜索功能
    search_columns = ['sn', 'ip', 'bmcip', 'adress','type','restart']

    # （可选）定义表单视图中包括哪些字段
    add_columns = ['sn', 'ip', 'bmcip', 'adress','type','restart']
    edit_columns = ['sn', 'ip', 'bmcip', 'adress','type','restart']



"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""
from flask_appbuilder.api import expose, BaseApi, ModelRestApi
from .models import BareMetal

def item_to_json(item):
    """将 BareMetal 对象转换为可序列化的字典"""
    return {
        'sn': item.sn,
        'ip': item.ip,
        'bmcip': item.bmcip,
        'adress': item.adress,
        'type': item.type,
        'restart': item.restart
    }

class BareMetalModelApi(BaseApi):

    resource_name = 'baremetal'
    datamodel = SQLAInterface(BareMetal)

    @expose('/getBareMetal', methods=["GET"])
    def get_item(self):
        items = db.session.query(BareMetal).all()
        result = [item_to_json(item) for item in items]

        return self.response(200, message=result)
        # item = db.session.query(BareMetal).filter_by(sn=sn).one_or_none()
        # if item is not None:
        #     return self.response(200, **item.to_json())
        # else:
        #     return self.response(404, message="Item not found")


    @expose('/restart/<string:bmc_ip>', methods=['POST'])
    def restart_bare_metal(self, bmc_ip):

        # 从请求体中获取重启原因
        data = request.json
        restart = data.get('reason', '')
        # 获取当前日期时间字符串，用于记录发生时间
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        user = "ADMIN"
        passwd = "Momenta00"
        try:
            # 寻找具有匹配 BMC IP 的记录
            bare_metal = db.session.query(BareMetal).filter_by(bmcip=bmc_ip).first()

            if bare_metal:
                # 检查是否已经有存储的重启原因并构建新的重启原因字符串
                updated_restart_reason = f"{bare_metal.restart}\n{timestamp}: {restart}" if bare_metal.restart.strip() else f"{timestamp}: {restart}"

                # 更新数据库记录
                bare_metal.restart = updated_restart_reason
                db.session.commit()
            else:
                # 如果没有找到记录，返回错误信息
                return self.response(404, message="No matching bare metal server found")

            # 运行 ipmitool 命令（略）
            # 执行重启操作...
                # 使用 subprocess.run 来执行 ipmitool 命令
            result = run(
                ["ipmitool", "-H", bmc_ip, "-U", user, "-P", passwd, "-I", "lanplus", "lan", "print"],
                check=True,
                stdout=PIPE,
                stderr=PIPE,
                text=True
            )

            if result.returncode == 0:
                # 返回成功响应
                return self.response(200, message="Machine is being restarted")
            else:
                return self.response(500, message="Failed to execute the restart command")


        except CalledProcessError as e:
            # 处理执行失败情况
            error_message = f"An error occurred: {e.stderr}"
            return self.response(500, message=error_message)

        except Exception as e:
            # 处理所有其他可能的错误
            error_message = f"An unexpected error occurred: {e}"
            return self.response(500, message=error_message)

        # 在这里进行权限验证和身份认证

        # 假设用户和密码是通过某种安全方式获取的，例如环境变量



@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


from flask_appbuilder.api import BaseApi, expose
from . import appbuilder


class ExampleApi(BaseApi):
    @expose('/greeting')
    def greeting(self):
        return self.response(200, message="Hello")


appbuilder.add_api(ExampleApi)


appbuilder.add_view(
    BareMetalModelView,
    "List BareMetal",  # 视图的显示名称
    icon="fa-folder-open-o",  # 视图的图标
    category="Management",  # 将视图放入名为 "Management" 的菜单分类
    category_icon="fa-cogs"  # 分类的图标
)

appbuilder.add_api(BareMetalModelApi)