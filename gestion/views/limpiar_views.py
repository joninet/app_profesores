from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def limpiar_mensajes(request):
    if request.method == "POST":
        storage = messages.get_messages(request)
        for _ in storage:  # Consumir los mensajes para eliminarlos
            pass
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)
