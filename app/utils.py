from fastapi import Response


def add_pagination_headers_to_response(response: Response, count: int, limit: int, offset: int) -> None:
    """Добавление заголовков пагинации к ответу"""

    response.headers["Pagination-Count"] = str(count)
    response.headers["Pagination-Limit"] = str(limit)
    response.headers["Pagination-Offset"] = str(offset)
