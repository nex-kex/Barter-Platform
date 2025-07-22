from django.shortcuts import render


def render_error(request, status_code, status_message, default_message):
    context = {"status_code": status_code, "status_message": status_message, "default_message": default_message}
    return render(request, "error.html", context=context, status=status_code)


def custom_permission_denied(request, exception):
    return render_error(
        request,
        status_code=403,
        status_message="Доступ запрещен",
        default_message="У вас нет прав для просмотра этой страницы.",
    )


def custom_page_not_found(request, exception):
    return render_error(
        request,
        status_code=404,
        status_message="Страница не найдена",
        default_message="Запрошенная страница не существует или была удалена.",
    )


def custom_error_handler(request, exception=None):
    return render_error(
        request,
        status_code=500,
        status_message="Ошибка сервера",
        default_message="Произошла внутренняя ошибка сервера.",
    )
