from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
)

server_extend_schema = extend_schema_view(
    list= extend_schema(
        parameters=[
            OpenApiParameter("category_id", OpenApiTypes.INT, description="Filter servers by category id"),
            OpenApiParameter("qty", OpenApiTypes.INT, description="Filter number of servers returned"),
            OpenApiParameter("num_member", OpenApiTypes.BOOL, description="Include member count for each server")
        ]
    )
)
server_user_extend_schema =extend_schema(
            parameters=[
                OpenApiParameter("category_id", OpenApiTypes.INT, description="Filter user's servers based on category id")
            ]
    )