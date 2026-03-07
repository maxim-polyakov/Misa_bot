from Deep_layer.NLP_package.Interfaces import IGpt
from openai import OpenAI
import logging
import time
import threading
from Deep_layer.DB_package.Classes import DB_Communication


def _conversation_key(user, chat_id=None):
    """Ключ для истории: (user, chat_id) или user для legacy."""
    return (user, chat_id) if chat_id else (user, None)


class Gpt(IGpt.IGpt):
    """
    It is a gpt text generator
    """
    __dbc = DB_Communication.DB_Communication()

    # Key: (user_id, chat_id), Value: {'history': list, 'start_time': float}
    _user_conversations = {}
    _cleanup_lock = threading.Lock()

    @classmethod
    def generate(cls, text, user, is_command_check=False, chat_id=None):
        # generating answers with conversation context
        # configuring logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")

        try:
            max_history = 100

            key = _conversation_key(user, chat_id)
            with cls._cleanup_lock:
                if key not in cls._user_conversations:
                    cls._user_conversations[key] = {
                        'history': [],
                        'start_time': time.time()
                    }

                user_data = cls._user_conversations[key]
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

            # System prompt: instruct GPT to format content in markdown blocks for proper display
            system_prompt = (
                "When you output code or structured content, always wrap it in markdown code blocks: "
                "```label\\ncontent\\n```. Use these labels for different frame styles:\n"
                "- Code: python, javascript, typescript, go, rust, java, etc.\n"
                "- json: JSON data\n"
                "- yaml/yml: YAML configs\n"
                "- bash/sh: shell commands\n"
                "- sql: SQL queries\n"
                "- md/markdown: Markdown snippets\n"
                "- diff: file diffs\n"
                "- warning: warnings\n"
                "- error: error messages\n"
                "- quote: citations\n"
                "- output: command output or logs"
            )
            api_messages = (
                [{"role": "user", "content": text}]
                if is_command_check
                else conversation_history
            )
            # При проверке команды — без системного сообщения (чистый запрос)
            messages = api_messages if is_command_check else [{"role": "system", "content": system_prompt}] + api_messages

            # sending a request to the gpt model to generate a response with full context
            response = client.chat.completions.create(
                model='gpt-4o',
                messages=messages,
                temperature=1,
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
                f'The gpt.generate method has completed successfully. User: {user}, Chat: {chat_id}, History length: {len(conversation_history)}, Command check: {is_command_check}')

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
                    keys_to_remove = []
                    for key, user_data in cls._user_conversations.items():
                        # Check if conversation is older than 3 hours
                        if (user_data['history'] and
                                current_time - user_data['start_time'] > 10800):  # 3 hours in seconds

                            old_length = len(user_data['history'])
                            user_data['history'] = []
                            user_data['start_time'] = current_time
                            logging.info(
                                f'Automatically cleaned up conversation history for {key}. Removed {old_length} messages.')

                        # Optional: Remove if history is empty for too long
                        if not user_data['history'] and current_time - user_data['start_time'] > 86400:  # 24 hours
                            keys_to_remove.append(key)

                    for key in keys_to_remove:
                        del cls._user_conversations[key]
                        logging.info(f'Removed inactive conversation: {key}')

        # Start the cleanup thread as daemon so it doesn't block program exit
        cleanup_thread = threading.Thread(target=cleanup_old_conversations, daemon=True)
        cleanup_thread.start()

    @classmethod
    def clear_conversation_history(cls, user=None, chat_id=None):
        """Clear conversation history for specific user/chat or all"""
        with cls._cleanup_lock:
            if user or chat_id:
                key = _conversation_key(user or '', chat_id)
                if key in cls._user_conversations:
                    old_length = len(cls._user_conversations[key]['history'])
                    cls._user_conversations[key]['history'] = []
                    cls._user_conversations[key]['start_time'] = time.time()
                    logging.info(f'Manually cleared conversation history for {key}. Removed {old_length} messages.')
                    return {"status": f"cleared {old_length} messages"}
                return {"status": "no history to clear"}
            else:
                total_messages = 0
                total_keys = len(cls._user_conversations)
                for user_data in cls._user_conversations.values():
                    total_messages += len(user_data['history'])
                    user_data['history'] = []
                    user_data['start_time'] = time.time()
                logging.info(f'Manually cleared all {total_keys} conversations. Removed {total_messages} messages.')
                return {"status": f"cleared {total_messages} messages from {total_keys} conversations"}

    @classmethod
    def get_conversation_history(cls, user=None, chat_id=None):
        """Get current conversation history for specific user/chat or all"""
        with cls._cleanup_lock:
            if user or chat_id:
                key = _conversation_key(user or '', chat_id)
                if key in cls._user_conversations:
                    return cls._user_conversations[key]['history']
                return []
            return {k: data['history'] for k, data in cls._user_conversations.items()}

    @classmethod
    def get_active_users(cls):
        """Get list of active (user, chat_id) with conversation history"""
        with cls._cleanup_lock:
            return list(cls._user_conversations.keys())

    @classmethod
    def import_history_from_db(cls, user, chat_id, exclude_last=0):
        """Импорт истории чата из БД в контекст GPT. exclude_last: исключить последние N сообщений."""
        try:
            from Core_layer.Chat_package.Classes.ChatService import ChatService
            messages = ChatService.get_messages(chat_id)
            if not messages:
                return
            if exclude_last > 0:
                messages = messages[:-exclude_last]
            key = _conversation_key(user, chat_id)
            history = []
            for m in messages:
                role = "user" if str(m.get('user', '')).strip() != 'Misa' else "assistant"
                content = str(m.get('content', '')).strip()
                if not content:
                    continue
                history.append({"role": role, "content": content})
            with cls._cleanup_lock:
                cls._user_conversations[key] = {
                    'history': history,
                    'start_time': time.time()
                }
            logging.info(f'Imported {len(history)} messages from DB for chat {chat_id}')
        except Exception as e:
            logging.warning(f'Failed to import history for chat {chat_id}: {e}')