from starlette_admin.contrib.sqla import Admin

from app.db.session import async_engine
from app.models import User
from app.admin.views import UserAdminView

admin = Admin(engine=async_engine, title="News API Admin", base_url="/admin")

admin.add_view(UserAdminView(User))
