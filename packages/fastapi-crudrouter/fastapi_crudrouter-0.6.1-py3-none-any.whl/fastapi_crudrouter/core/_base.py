from typing import Any, Callable, Generic, List, Optional, Type

from fastapi import APIRouter, HTTPException
from fastapi.types import DecoratedCallable

from ._types import T
from ._utils import pagination_factory, schema_factory

NOT_FOUND = HTTPException(404, "Item not found")


class CRUDGenerator(Generic[T], APIRouter):
    schema: Type[T]
    create_schema: Type[T]
    update_schema: Type[T]
    _base_path: str = "/"

    def __init__(
        self,
        schema: Type[T],
        create_schema: Optional[Type[T]] = None,
        update_schema: Optional[Type[T]] = None,
        prefix: Optional[str] = None,
        paginate: Optional[int] = None,
        get_all_route: bool = True,
        get_one_route: bool = True,
        create_route: bool = True,
        update_route: bool = True,
        delete_one_route: bool = True,
        delete_all_route: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:

        self.schema = schema
        self.pagination = pagination_factory(max_limit=paginate)
        self._pk: str = self._pk if hasattr(self, "_pk") else "id"
        self.create_schema = (
            create_schema
            if create_schema
            else schema_factory(self.schema, pk_field_name=self._pk, name="Create")
        )
        self.update_schema = (
            update_schema
            if update_schema
            else schema_factory(self.schema, pk_field_name=self._pk, name="Update")
        )

        prefix = str(self.schema.__name__.lower() if not prefix else prefix)
        prefix = self._base_path + prefix.strip("/")
        super().__init__(
            prefix=prefix, tags=[prefix.strip("/").capitalize()], *args, **kwargs
        )

        if get_all_route:
            super().add_api_route(
                "",
                self._get_all(),
                methods=["GET"],
                response_model=Optional[List[self.schema]],  # type: ignore
                summary="Get All",
            )

        if create_route:
            super().add_api_route(
                "",
                self._create(),
                methods=["POST"],
                response_model=self.schema,
                summary="Create One",
            )

        if delete_all_route:
            super().add_api_route(
                "",
                self._delete_all(),
                methods=["DELETE"],
                response_model=Optional[List[self.schema]],  # type: ignore
                summary="Delete All",
            )

        if get_one_route:
            super().add_api_route(
                "/{item_id}",
                self._get_one(),
                methods=["GET"],
                response_model=self.schema,
                summary="Get One",
            )

        if update_route:
            super().add_api_route(
                "/{item_id}",
                self._update(),
                methods=["PUT"],
                response_model=self.schema,
                summary="Update One",
            )

        if delete_one_route:
            super().add_api_route(
                "/{item_id}",
                self._delete_one(),
                methods=["DELETE"],
                response_model=self.schema,
                summary="Delete One",
            )

    def api_route(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """ Overrides and exiting route if it exists"""
        methods = kwargs["methods"] if "methods" in kwargs else ["GET"]
        self.remove_api_route(path, methods)
        return super().api_route(path, *args, **kwargs)

    def get(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["Get"])
        return super().get(path, *args, **kwargs)

    def post(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["POST"])
        return super().post(path, *args, **kwargs)

    def put(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["PUT"])
        return super().put(path, *args, **kwargs)

    def delete(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["DELETE"])
        return super().delete(path, *args, **kwargs)

    def remove_api_route(self, path: str, methods: List[str]) -> None:
        methods_ = set(methods)

        for route in self.routes:
            if (
                route.path == f"{self.prefix}{path}"  # type: ignore
                and route.methods == methods_  # type: ignore
            ):
                self.routes.remove(route)

    def _get_all(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    def _get_one(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    def _create(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    def _update(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    def _delete_one(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    def _delete_all(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    @staticmethod
    def get_routes() -> List[str]:
        return ["get_all", "create", "delete_all", "get_one", "update", "delete_one"]
