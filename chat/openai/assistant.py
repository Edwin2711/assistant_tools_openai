from django.conf import settings
from openai import OpenAI
from .tools import available_tools, get_product_info, check_stock
import json

class assistant:
    def __init__(self):
        print("Initializing assistant")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.assistant_id = self._create_assistant()
        self.thread_id = self._create_thread()

    def get_response(self, message):
        """
        Get the response from the AI assistant for the given user message.

        Args:
            message (str): The message from the user.

        Returns:
            str: The response from the AI assistant.
        """
        try:
            # Add the user message to the thread
            thread_message = self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="user",
                content=message
            )

            # Create and poll for the AI assistant's response
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id
            )

            # Get the response from the AI assistant
            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id
                )
                response = messages.data[0].content[0].text.value
            else:
                print("Run status: ",run.status)

                # If the AI assistant requires an action, we need to call the tools
                if run.status == 'requires_action':
                    response = self._calling_tools(run)

            # Add the AI assistant's response to the thread
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="assistant",
                content=response
            )

        except Exception as e:
            print(e)
            response = "Sorry my mistake"
        return response
    
    def _create_assistant(self):
        prompt = """You are a shop assistant who can answer questions about products and help customers with their purchases.
        You sell this products: laptop_pro, smartphone_plus, wireless_earbuds, smart_watch, tablet_lite. When user ask about a product,
        you should use the tools get_product_info and check_stock to answer the user's questions."""
        tools = available_tools()
        my_assistant = self.client.beta.assistants.create(
            instructions=prompt,
            name="ShopBot",
            tools=tools,
            model="gpt-4o",
        )
        
        return my_assistant.id
    
    def _create_thread(self):
        my_thread = self.client.beta.threads.create()
        
        return my_thread.id
    
    def _calling_tools(self, run):
        print("Calling tools")
        # Define the list to store tool outputs
        tool_outputs = []
        # Loop through each tool in the required action section
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "get_product_info":
                # Call the get_product_info function
                args = json.loads(tool.function.arguments)
                tool_response = get_product_info(**args)
                tool_outputs.append({
                "tool_call_id": tool.id,
                "output": tool_response
                })
            elif tool.function.name == "check_stock":
                # Call the check_stock function
                args = json.loads(tool.function.arguments)
                tool_response = check_stock(**args)
                tool_outputs.append({
                "tool_call_id": tool.id,
                "output": tool_response
                })
        # Submit all tool outputs at once after collecting them in a list
        if tool_outputs:
            try:
                run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=self.thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
            except Exception as e:
                print("Failed to submit tool outputs:", e)
        else:
            print("No tool outputs to submit.")
        
        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread_id
            )
            response = messages.data[0].content[0].text.value
            return response
        else:
            print("New run status: ",run.status)
            print("New run: ", run)