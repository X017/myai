# views.py
import ollama
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# store chat history per session (simple example)
# in production, you may want to use DB or cache
SESSION_KEY = "chat_history"

class OllamaChatView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        # render chat page
        request.session.flush()
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # get user message
        import json
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
            user_message = payload.get("message", "").strip()
        except Exception:
            user_message = request.POST.get("message", "").strip()

        if not user_message:
            return JsonResponse({"error": "No message provided"}, status=400)

        # get chat history from session
        messages = request.session.get(SESSION_KEY, [])

        # append user message
        messages.append({"role": "user", "content": user_message})

        # call Ollama
        try:
            response = ollama.chat(
                model="llama2",
                messages=messages
            )
            reply = response.get("message", {}).get("content", "")
        except Exception as e:
            reply = f"[Error contacting Ollama: {e}]"

        if reply:
            messages.append({"role": "assistant", "content": reply})

        # save updated messages in session
        request.session[SESSION_KEY] = messages

        return JsonResponse({"reply": reply})
