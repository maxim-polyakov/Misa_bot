import yt_dlp
import asyncio
import disnake
import logging
import urllib.parse, urllib.request, re
from typing import Optional, Any
from Core_layer.Bot_package.Interfaces import IMonitor


class SongsMonitor(IMonitor.IMonitor):
    """

    It is class for playing music

    """

    queues = {}
    voice_clients = {}
    youtube_base_url = 'https://www.youtube.com/'
    youtube_results_url = youtube_base_url + 'results?'
    youtube_watch_url = youtube_base_url + 'watch?v='
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn -filter:a "volume=0.25"'}
    yt_dl_options = {
        "format": "bestaudio",
        "extractor_args": {"youtube": {"formats": "missing_pot"}},
        "socket_timeout": 10,
        "extract_flat": False,
        "ignoreerrors": "only_download"
    }
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    @classmethod
    async def __play_next(cls, bot, message):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            gid = message.guild.id
            if gid not in cls.queues or cls.queues[gid] == []:
                return
            link = cls.queues[gid].pop(0)
            sm = SongsMonitor(bot, message)
            await sm.monitor(link)
        except Exception:
            logging.exception('The exception occurred in songsmonitor.__play_next')

    def _sync_voice_client_map(self):
        guild = getattr(self.message, "guild", None)
        if not guild:
            return
        vc = guild.voice_client
        if vc is not None:
            SongsMonitor.voice_clients[guild.id] = vc
        else:
            SongsMonitor.voice_clients.pop(guild.id, None)

    async def _wait_for_voice_live(self, guild, max_wait: float = 10.0) -> Any:
        """Подождать, пока голос снова станет connected (после yt-dlp бывают краткие ложные «обрывы»)."""
        loop = asyncio.get_running_loop()
        deadline = loop.time() + max_wait
        while loop.time() < deadline:
            vc = guild.voice_client
            if vc is not None:
                try:
                    if vc.is_connected():
                        return vc
                except Exception:
                    pass
            await asyncio.sleep(0.25)
        vc = guild.voice_client
        if vc is not None:
            try:
                if vc.is_connected():
                    return vc
            except Exception:
                pass
        return None

    @classmethod
    def _resolve_play_url_sync(cls, initial: str) -> Optional[str]:
        """
        Синхронно: URL watch или None. Только из run_in_executor —
        иначе urllib блокирует event loop и рвётся голос Discord.
        """
        s = (initial or "").strip()
        if not s:
            return None
        if cls.youtube_base_url in s:
            return s
        query_string = urllib.parse.urlencode({"search_query": s})
        req = cls.youtube_results_url + query_string
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode()
        found = re.findall(r"/watch\?v=(.{11})", body)
        if not found:
            return None
        return cls.youtube_watch_url + found[0]

    async def join(self):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if self.message.author.voice is None:
                return 'вы не подключены к голосовому каналу'
            target = self.message.author.voice.channel
            permissions = target.permissions_for(target.guild.me)
            if not permissions.connect:
                return 'невозможно подключится к данному каналу'

            guild = self.message.guild
            vc = guild.voice_client
            # Не рвём сессию сразу: при кратковременном False is_connected() disconnect() сам «выкидывает» бота из канала.
            if vc is not None and not vc.is_connected():
                recovered = await self._wait_for_voice_live(guild, max_wait=6.0)
                if recovered is not None:
                    vc = recovered
                else:
                    vc = guild.voice_client
                    if vc is not None and not vc.is_connected():
                        try:
                            await vc.disconnect(force=True)
                        except Exception:
                            pass
                        SongsMonitor.voice_clients.pop(guild.id, None)
                        vc = None

            if vc is not None:
                if vc.channel != target:
                    await vc.move_to(target)
                    await asyncio.sleep(0.5)
                self._sync_voice_client_map()
                logging.info('The songsmonitor.join method has completed successfully (existing or moved)')
                return 'подключился к голосовому каналу'

            # connect() уже дожидается готового соединения — не проверяем is_connected() отдельно
            # (ложный таймаут рвёт сессию и даёт «не удалось установить голосовое соединение»).
            await target.connect(timeout=120.0, reconnect=True)
            self._sync_voice_client_map()
            vc_new = guild.voice_client
            if vc_new is None:
                logging.warning('songsmonitor.join: guild.voice_client is None after connect')
                return 'не удалось установить голосовое соединение'
            SongsMonitor.voice_clients[guild.id] = vc_new
            logging.info('The songsmonitor.join method has completed successfully')
            return 'подключился к голосовому каналу'
        except Exception as e:
            logging.exception('The exception occurred in songsmonitor.join: ' + str(e))
            err = str(e)
            if 'Already connected' in err:
                self._sync_voice_client_map()
                return 'бот уже подключен к голосовому каналу'
            return e

    async def leave(self):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            server = self.message.guild
            voice_client = server.voice_client
            if voice_client == None:
                return 'бот не подключен к голосовому каналу'
            await voice_client.disconnect()
            SongsMonitor.voice_clients.pop(self.message.guild.id, None)
            logging.info('The songsmonitor.leave method has completed successfully')
            return 'отключился от голосового канала'
        except Exception as e:
            logging.exception('The exception occurred in songsmonitor.leave: ' + str(e))
            return e

    async def queue(self, url):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            gid = self.message.guild.id
            if gid not in SongsMonitor.queues:
                SongsMonitor.queues[gid] = []
            SongsMonitor.queues[gid].append(url)
            logging.info('The songsmonitor.queue method has completed successfully')
            return 'добавлено в очередь!'
        except Exception as e:
            logging.exception('The exception occurred in songsmonitor.queue: ' + str(e))
            return e

    async def stop(self):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            voice_client = self.message.guild.voice_client
            if voice_client == None:
                return 'бот ничего не проигрывает в данный момент.'
            else:
                if voice_client.is_playing():
                    SongsMonitor.voice_clients[self.message.guild.id].stop()
                    logging.info('The songsmonitor.pause method has completed successfully')
                    return 'готово'
                else:
                    logging.info('The songsmonitor.pause method has completed successfully')
                    return 'бот ничего не проигрывает в данный момент.'
        except Exception as e:
            logging.exception('The exception occurred in songsmonitor.stop: ' + str(e))
            return e

    async def pause(self):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            voice_client = self.message.guild.voice_client
            if voice_client == None:
                return 'бот ничего не проигрывает в данный момент.'
            else:
                if voice_client.is_playing():
                    SongsMonitor.voice_clients[self.message.guild.id].pause()
                    logging.info('The songsmonitor.pause method has completed successfully')
                    return 'готово'
                else:
                    logging.info('The songsmonitor.pause method has completed successfully')
                    return 'бот ничего не проигрывает в данный момент.'
        except Exception as e:
            logging.exception('The exception occurred in songsmonitor.pause: ' + str(e))
            return e

    async def resume(self):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            voice_client = self.message.guild.voice_client
            if voice_client == None:
                return 'бот ничего не проигрывает в данный момент.'
            else:
                SongsMonitor.voice_clients[self.message.guild.id].resume()
                logging.info('The songsmonitor.resume method has completed successfully')
                return 'бот возобновил проигрывание музыки'

        except Exception as e:
            logging.exception('The exception occurred in songsmonitor.resume: ' + str(e))
            return e

    async def monitor(self, url):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()

            j0 = await self.join()
            if not isinstance(j0, str):
                return f'не удалось войти в голос: {j0}'
            if 'подключился' not in j0 and 'уже подключен' not in j0:
                return j0

            play_url = (url or "").strip()
            play_url = await loop.run_in_executor(None, self._resolve_play_url_sync, play_url)
            if not play_url:
                return 'по запросу ничего не найдено на YouTube'

            def _extract():
                return SongsMonitor.ytdl.extract_info(play_url, download=False)

            data = await loop.run_in_executor(None, _extract)
            if data is None:
                return 'не удалось получить данные о видео (yt-dlp вернул None)'

            song = data.get('url')
            if not song:
                return 'не удалось извлечь аудиопоток (обновите yt-dlp: pip install -U yt-dlp)'

            self._sync_voice_client_map()
            guild = self.message.guild
            guild_id = guild.id
            voice_client = await self._wait_for_voice_live(guild, max_wait=8.0)
            if voice_client is None:
                j = await self.join()
                if isinstance(j, str) and (
                    'подключился' in j or 'уже подключен' in j
                ):
                    self._sync_voice_client_map()
                    voice_client = guild.voice_client
                else:
                    return (
                        'голосовое соединение потеряно во время подготовки трека. '
                        f'Повторите /join: {j}'
                    )
            if voice_client is None or not voice_client.is_connected():
                voice_client = await self._wait_for_voice_live(guild, max_wait=3.0)
            if voice_client is None or not voice_client.is_connected():
                return 'бот не подключен к голосовому каналу'

            vc_now = guild.voice_client
            if vc_now is not None:
                voice_client = vc_now

            await asyncio.sleep(0.25)

            msg = self.message
            bot = self.bot

            player = disnake.FFmpegOpusAudio(song, **SongsMonitor.ffmpeg_options)
            try:
                voice_client.play(
                    player,
                    after=lambda e, _loop=loop, m=msg, b=bot: asyncio.run_coroutine_threadsafe(
                        SongsMonitor.__play_next(b, m), _loop
                    ),
                )
            except Exception as play_err:
                logging.exception('songsmonitor.monitor play failed: %s', play_err)
                return f'не удалось начать воспроизведение: {play_err}'

            SongsMonitor.voice_clients[guild_id] = voice_client
            logging.info('The songsmonitor.monitor method has completed successfully')
            return 'готово'
        except Exception as e:
            logging.exception('The exception occurred in songsmonitor.monitor: ' + str(e))
            if str(e) == 'Already playing audio.':
                return 'бот уже проигрывает музыку.'
            else:
                if str(e) == self.message.guild.id:
                    return 'id гильдии не найден в списке, бот не подключен к голосовому каналу'
                else:
                    if str(e) == 'Not connected to voice.':
                        return "бот не подключён к голосовому каналу"
                    else:
                        return e
