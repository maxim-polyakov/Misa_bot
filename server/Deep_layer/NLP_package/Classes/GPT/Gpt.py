from Deep_layer.NLP_package.Interfaces import IGpt
from openai import OpenAI
import logging
import time
import threading
from Deep_layer.DB_package.Classes import DB_Communication

class Gpt(IGpt.IGpt):
    """
    It is a gpt text generator
    """
    __dbc = DB_Communication.DB_Communication()

    @classmethod
    def generate(cls, text, max_history=100, is_command_check=False):
        # generating answers with conversation context
        # configuring logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")

        try:
            # Initialize conversation history storage if not exists
            if not hasattr(cls, '_conversation_history'):
                cls._conversation_history = []
                cls._conversation_start_time = time.time()
                # Start cleanup thread
                cls._start_cleanup_thread()

            # Retrieve conversation history
            conversation_history = cls._conversation_history

            # Only add to history if this is NOT a command check
            if not is_command_check:
                # Add new user message to history
                conversation_history.append({
                    "role": "user",
                    "content": text,
                })

                # Limit history length to prevent token overflow
                if len(conversation_history) > max_history * 2:
                    conversation_history = conversation_history[-(max_history * 2):]

            # retrieving api tokens from the database
            fdf = cls.__dbc.get_data(
                'select token from assistant_sets.tokens where botname = \'Misa\' and platformname = \'Gpt\'')
            sdf = cls.__dbc.get_data(
                'select token from assistant_sets.projects where botname = \'Misa\' and platformname = \'Gpt\'')
            tdf = cls.__dbc.get_data(
                'select token from assistant_sets.organizations where botname = \'Misa\' and platformname = \'Gpt\'')
            # extracting api keys from the retrieved data
            OPENAI_API_KEY = fdf['token'][0]
            OPENAI_API_PROJECT = sdf['token'][0]
            OPENAI_API_ORG = tdf['token'][0]
            # initializing openai client with api credentials
            client = OpenAI(
                api_key=OPENAI_API_KEY,
                organization=OPENAI_API_ORG,
                project=OPENAI_API_PROJECT,
            )

            # sending a request to the gpt model to generate a response with full context
            response = client.chat.completions.create(
                model='chatgpt-4o-latest',
                messages=conversation_history if not is_command_check else [{"role": "user", "content": text}],
                temperature=0,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Extract assistant response
            assistant_response = response.choices[0].message.content

            # Only add to history if this is NOT a command check
            if not is_command_check:
                # Add assistant response to conversation history
                conversation_history.append({
                    "role": "assistant",
                    "content": assistant_response,
                })

                # Update stored history
                cls._conversation_history = conversation_history

            # logging successful completion of the method
            logging.info(
                f'The gpt.generate method has completed successfully. History length: {len(conversation_history)}, Command check: {is_command_check}')

            # returning the generated response
            return {
                "response": assistant_response,
                "history_length": len(conversation_history) if not is_command_check else 0,
                "is_command_check": is_command_check
            }

        except Exception as e:
            # logging any exceptions that occur during execution
            logging.exception('The exception occurred in gpt.generate: ' + str(e))
            return {
                "response": f"Sorry, an error occurred: {str(e)}",
                "error": True
            }

    @classmethod
    def _start_cleanup_thread(cls):
        """Start background thread for automatic cleanup"""

        def cleanup_old_conversations():
            while True:
                time.sleep(3600)  # Check every hour
                current_time = time.time()

                # Check if conversation is older than 3 hours
                if (hasattr(cls, '_conversation_start_time') and
                        hasattr(cls, '_conversation_history') and
                        cls._conversation_history and
                        current_time - cls._conversation_start_time > 10800):  # 3 hours in seconds

                    old_length = len(cls._conversation_history)
                    cls._conversation_history = []
                    cls._conversation_start_time = current_time
                    logging.info(f'Automatically cleaned up conversation history. Removed {old_length} messages.')

        # Start the cleanup thread as daemon so it doesn't block program exit
        cleanup_thread = threading.Thread(target=cleanup_old_conversations, daemon=True)
        cleanup_thread.start()

    @classmethod
    def clear_conversation_history(cls):
        """Clear conversation history"""
        if hasattr(cls, '_conversation_history'):
            old_length = len(cls._conversation_history)
            cls._conversation_history = []
            cls._conversation_start_time = time.time()
            logging.info(f'Manually cleared conversation history. Removed {old_length} messages.')
            return {"status": f"cleared {old_length} messages from history"}
        else:
            return {"status": "no history to clear"}

    @classmethod
    def get_conversation_history(cls):
        """Get current conversation history"""
        if not hasattr(cls, '_conversation_history'):
            return []

        return cls._conversation_history
