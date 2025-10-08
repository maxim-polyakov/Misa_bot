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

    # Используем словарь для хранения истории диалогов для каждого пользователя
    _user_conversations = {}  # Key: user_id, Value: {'history': list, 'start_time': float}
    _cleanup_lock = threading.Lock()

    @classmethod
    def generate(cls, text, user, is_command_check=False):
        # generating answers with conversation context
        # configuring logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")

        try:
            max_history = 100

            # Инициализируем или получаем историю диалога для конкретного пользователя
            with cls._cleanup_lock:
                if user not in cls._user_conversations:
                    cls._user_conversations[user] = {
                        'history': [],
                        'start_time': time.time()
                    }

                user_data = cls._user_conversations[user]
                conversation_history = user_data['history']

            # Start cleanup thread if not already running
            if not hasattr(cls, '_cleanup_thread_started'):
                cls._start_cleanup_thread()
                cls._cleanup_thread_started = True

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
                    user_data['history'] = conversation_history

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

            # logging successful completion of the method
            logging.info(
                f'The gpt.generate method has completed successfully. User: {user}, History length: {len(conversation_history)}, Command check: {is_command_check}')

            # returning the generated response
            return assistant_response

        except Exception as e:
            # logging any exceptions that occur during execution
            logging.exception('The exception occurred in gpt.generate: ' + str(e))
            return {
                "response": f"Sorry, an error occurred: {str(e)}",
                "error": True
            }

    @classmethod
    def _start_cleanup_thread(cls):
        """Start background thread for automatic cleanup of all user conversations"""

        def cleanup_old_conversations():
            while True:
                time.sleep(3600)  # Check every hour
                current_time = time.time()

                with cls._cleanup_lock:
                    users_to_remove = []
                    for user_id, user_data in cls._user_conversations.items():
                        # Check if conversation is older than 3 hours
                        if (user_data['history'] and
                                current_time - user_data['start_time'] > 10800):  # 3 hours in seconds

                            old_length = len(user_data['history'])
                            user_data['history'] = []
                            user_data['start_time'] = current_time
                            logging.info(
                                f'Automatically cleaned up conversation history for user {user_id}. Removed {old_length} messages.')

                        # Optional: Remove user data entirely if history is empty for too long
                        # This prevents memory leaks from inactive users
                        if not user_data['history'] and current_time - user_data['start_time'] > 86400:  # 24 hours
                            users_to_remove.append(user_id)

                    # Remove inactive users
                    for user_id in users_to_remove:
                        del cls._user_conversations[user_id]
                        logging.info(f'Removed inactive user data for: {user_id}')

        # Start the cleanup thread as daemon so it doesn't block program exit
        cleanup_thread = threading.Thread(target=cleanup_old_conversations, daemon=True)
        cleanup_thread.start()

    @classmethod
    def clear_conversation_history(cls, user=None):
        """Clear conversation history for specific user or all users"""
        with cls._cleanup_lock:
            if user:
                # Clear history for specific user
                if user in cls._user_conversations:
                    old_length = len(cls._user_conversations[user]['history'])
                    cls._user_conversations[user]['history'] = []
                    cls._user_conversations[user]['start_time'] = time.time()
                    logging.info(
                        f'Manually cleared conversation history for user {user}. Removed {old_length} messages.')
                    return {"status": f"cleared {old_length} messages from history for user {user}"}
                else:
                    return {"status": f"no history to clear for user {user}"}
            else:
                # Clear history for all users
                total_messages = 0
                total_users = len(cls._user_conversations)
                for user_data in cls._user_conversations.values():
                    total_messages += len(user_data['history'])
                    user_data['history'] = []
                    user_data['start_time'] = time.time()

                logging.info(
                    f'Manually cleared conversation history for all {total_users} users. Removed {total_messages} total messages.')
                return {"status": f"cleared {total_messages} messages from {total_users} users"}

    @classmethod
    def get_conversation_history(cls, user=None):
        """Get current conversation history for specific user or all users"""
        with cls._cleanup_lock:
            if user:
                # Get history for specific user
                if user in cls._user_conversations:
                    return cls._user_conversations[user]['history']
                else:
                    return []
            else:
                # Return all users' history
                return {user_id: data['history'] for user_id, data in cls._user_conversations.items()}

    @classmethod
    def get_active_users(cls):
        """Get list of active users with conversation history"""
        with cls._cleanup_lock:
            return list(cls._user_conversations.keys())