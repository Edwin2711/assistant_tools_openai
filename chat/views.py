from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .openai.assistant import assistant

ecommerce_assistant = assistant()

def chat_view(request):
    """
    View for the chat interface.

    This view renders the HTML template for the chat interface.
    """
    return render(request, 'chat.html')

@csrf_exempt
def send_message(request):
    """
    Handles incoming POST requests with a message from the user.

    The view processes the message and sends a response back to the user.
    """
    if request.method == 'POST':
        # Get the message from the request body
        data = json.loads(request.body)
        user_message = data.get('message', '')

        try:
            # Get the response from the OpenAI assistant
            response = ecommerce_assistant.get_response(user_message)
            
            # Return the response as a JSON object
            return JsonResponse({
                'message': response,
                'status': 'success'
            })
            
        except Exception as e:
            # Handle any exceptions that may occur
            print(e)
            return JsonResponse({
                'message': 'Sorry, there was an error processing your request.',
                'status': 'error'
            })

    # Return an error JSON object for invalid requests
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
