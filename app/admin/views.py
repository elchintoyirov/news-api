from starlette_admin.contrib.sqla import ModelView


class UserAdminView(ModelView):
    fields = [
        "id",
        "email",
        "password_hash",
        "first_name",
        "last_name",
        "profession_id",
        "bio",
        "posts_count",
        "posts_read_count",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_deleted",
        "deleted_email",
        "created_at",
        "updated_at",
    ]

    exclude_fields_from_list = [
        "password_hash",
        "bio",
        "posts_count",
        "posts_read_count",
        "is_deleted",
        "deleted_email",
    ]

    exclude_fields_from_detail = []

    exclude_fields_from_create = [
        "id",
        "created_at",
        "updated_at",
        "posts_count",
        "posts_read_count",
    ]

    exclude_fields_from_edit = ["id", "password_hash", "created_at", "updated_at"]
