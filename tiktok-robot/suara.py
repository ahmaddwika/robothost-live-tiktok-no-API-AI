# ==========================================================
#  MODUL SUARA (TTS + PEMUTAR AUDIO + AVATAR)
#  Mengubah teks menjadi suara (Edge-TTS).
#  Audio diambil oleh avatar di browser OBS (untuk lip-sync).
# ==========================================================

import asyncio
import os
import sys
import time

import edge_tts

import config

# --- Mode putar audio ---
# "browser" = avatar di OBS yang memutar suara (lip-sync bergerak)
# "speaker" = suara keluar dari speaker komputer langsung (tanpa avatar)
MODE_AUDIO = "browser"
SERVER_URL = "http://127.0.0.1:8765"

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# File subtitle untuk ditampilkan di OBS (browser source)
SUBTITLE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subtitle.txt")

_counter = 0
_pygame = None
_server_mod = None


def set_server(modul):
    """Daftarkan modul server agar state avatar bisa diperbarui."""
    global _server_mod
    _server_mod = modul


def _get_pygame():
    global _pygame
    if _pygame is None:
        import pygame
        pygame.mixer.init()
        _pygame = pygame
    return _pygame


def _tulis_subtitle(teks: str):
    """Tulis teks terakhir ke file subtitle.txt (dibaca OBS)."""
    try:
        with open(SUBTITLE_FILE, "w", encoding="utf-8") as f:
            f.write(teks)
    except Exception:
        pass


def _durasi_mp3(path: str) -> float:
    """Durasi tepat (detik) pakai mutagen, fallback ke estimasi ukuran."""
    try:
        from mutagen.mp3 import MP3
        return MP3(path).info.length
    except Exception:
        try:
            return os.path.getsize(path) / 4000.0
        except Exception:
            return 2.0


async def _generate_plain(text: str, out_path: str):
    communicate = edge_tts.Communicate(
        text,
        voice=config.VOICE,
        rate=config.VOICE_RATE,
        pitch=config.VOICE_PITCH,
        volume=config.VOICE_VOLUME,
    )
    await communicate.save(out_path)


def _escape_xml(t: str) -> str:
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


async def _generate(text: str, out_path: str, gaya: str = ""):
    """Hasilkan audio dengan emosi.
    Edge-TTS tidak mendukung <mstts:express-as>, jadi emosi dibuat
    dari kombinasi rate/pitch/volume (yang didukung).
    """
    prof = _profil_gaya(gaya)
    communicate = edge_tts.Communicate(
        text,
        voice=config.VOICE,
        rate=prof["rate"],
        pitch=prof["pitch"],
        volume=prof["volume"],
    )
    await communicate.save(out_path)


# Profil emosi: (rate, pitch, volume) - disamakan biar suara lebih konsisten
_PROFIL = {
    "cheerful":   {"rate": config.VOICE_RATE, "pitch": config.VOICE_PITCH, "volume": config.VOICE_VOLUME},
    "excited":    {"rate": config.VOICE_RATE, "pitch": config.VOICE_PITCH, "volume": config.VOICE_VOLUME},
    "friendly":   {"rate": config.VOICE_RATE, "pitch": config.VOICE_PITCH, "volume": config.VOICE_VOLUME},
    "empathetic": {"rate": config.VOICE_RATE, "pitch": config.VOICE_PITCH, "volume": config.VOICE_VOLUME},
    "calm":       {"rate": config.VOICE_RATE, "pitch": config.VOICE_PITCH, "volume": config.VOICE_VOLUME},
    "happy":      {"rate": config.VOICE_RATE, "pitch": config.VOICE_PITCH, "volume": config.VOICE_VOLUME},
    "talk":       {"rate": config.VOICE_RATE, "pitch": config.VOICE_PITCH, "volume": config.VOICE_VOLUME},
}


def _profil_gaya(gaya: str) -> dict:
    base = {
        "rate": config.VOICE_RATE,
        "pitch": config.VOICE_PITCH,
        "volume": config.VOICE_VOLUME,
    }
    return base


def ucapkan(text: str, tampilkan_subtitle: bool = True, gaya: str = "",
            effect: str = ""):
    """Ubah teks jadi suara lalu tampilkan/pentalkan ke avatar.
    gaya   : emosi bicara (cheerful, friendly, excited, empathetic, ...)
    effect : efek visual di avatar (birthday, doa, ...)
    """
    global _counter
    if not text or not text.strip():
        return

    _counter += 1
    nama_file = f"ucap_{_counter}.mp3"
    out_path = os.path.join(AUDIO_DIR, nama_file)

    try:
        asyncio.run(_generate(text, out_path, gaya))
    except Exception as e:
        print(f"[TTS ERROR] {e}")
        # fallback tanpa SSML
        try:
            asyncio.run(_generate_plain(text, out_path))
        except Exception as e2:
            print(f"[TTS ERROR-2] {e2}")
            return

    if tampilkan_subtitle:
        _tulis_subtitle(text)

    if MODE_AUDIO == "browser" and _server_mod is not None:
        durasi = _durasi_mp3(out_path)
        # Token unik: counter + timestamp -> tetap unik walau server di-restart
        token = f"{_counter}-{int(time.time() * 1000)}"
        mood = "happy" if gaya in ("cheerful", "excited", "happy") else "talk"
        _server_mod.set_state(
            speaking=True, text=text,
            audio=f"/audio/{nama_file}",
            token=token,
            effect=effect,
            mood=mood, ts=time.time(),
        )
        time.sleep(durasi + config.JEDA_ANTAR_UCAPAN)
        _server_mod.set_state(speaking=False, mood="idle", ts=time.time())
    else:
        # Fallback: putar lewat speaker komputer langsung
        pg = _get_pygame()
        try:
            pg.mixer.music.load(out_path)
            pg.mixer.music.play()
            while pg.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            print(f"[AUDIO ERROR] {e}")
        finally:
            try:
                pg.mixer.music.unload()
                time.sleep(config.JEDA_ANTAR_UCAPAN)
            except Exception:
                pass


def cek_voice_tersedia():
    """Tampilkan daftar suara bahasa Indonesia yang tersedia."""
    async def _list():
        voices = await edge_tts.list_voices()
        for v in voices:
            if v["Locale"].startswith("id-"):
                print(f"  {v['ShortName']}  ({v['Gender']})")
    asyncio.run(_list())
