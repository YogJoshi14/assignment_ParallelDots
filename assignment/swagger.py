from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path
from django.http import HttpResponse
import yaml

schema_view = get_schema_view(
    openapi.Info(
        title="Image Matching API",
        default_version='v1',
        description="API for uploading two images and appling matching algorithm on them",
        terms_of_service="",
        contact=openapi.Contact(email="yogjoshi14@gmail.com"),
        license=openapi.License(name="OPEN"),
    ),
    public=True,
)

# Generate the OpenAPI schema (swagger.yaml) and return it as a response
def schema_view_yaml(request):
    generator = schema_view.generator_class(schema_view.info)
    swagger_yaml = generator.get_schema(request=request, public=True)
    return HttpResponse(yaml.dump(swagger_yaml), content_type="text/plain")

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
