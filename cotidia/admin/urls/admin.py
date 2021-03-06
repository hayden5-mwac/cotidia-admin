from django.urls import path

from cotidia.admin.views.generic import (
    AdminOrderableView,
    AdminGenericSearchView,
    AdminGenericExportView,
    DynamicListView,
    AdminGenericStatusHistoryView,
)

app_name = "cotidia.admin"

urlpatterns = [
    path(
        "order/<int:content_type_id>/<int:object_id>",
        AdminOrderableView.as_view(),
        name="order",
    ),
    path(
        "dynamic-list/<str:app_label>/<str:model>",
        DynamicListView.as_view(),
        name="list",
    ),
    path("search", AdminGenericSearchView.as_view(), name="search"),
    path(
        "export/<str:app_label>/<str:model>/csv",
        AdminGenericExportView.as_view(),
        {"format": "csv"},
        name="export-csv",
    ),
    path(
        "export/<str:app_label>/<str:model>/pdf",
        AdminGenericExportView.as_view(),
        {"format": "pdf"},
        name="export-pdf",
    ),
    path(
        "status/history/<str:app_label>/<str:model>/<int:object_id>/<str:taxonomy>",
        AdminGenericStatusHistoryView.as_view(),
        name="status-history",
    ),
    path(
        "status/history/<str:app_label>/<str:model>/<int:object_id>",
        AdminGenericStatusHistoryView.as_view(),
        name="status-history",
    ),
]
