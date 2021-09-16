from rest_framework import mixins
from rest_framework.response import Response


class ListModelMixin(mixins.ListModelMixin):
    # def get_paginated_response(self,data):
    #     pass

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        meta = None
        if self.paginator:
            data = response.data.pop('results')
            meta = response.data
        else:
            data = response.data

        result = {
            "data": data,
        }
        if meta:
            result.update(
                {"meta": meta}
            )
        return Response(result)


class RetrieveModelMixin(mixins.RetrieveModelMixin):

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({"data": response.data})


class CreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"data": response.data})
