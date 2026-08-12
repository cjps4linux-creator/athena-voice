#!/usr/bin/env python3
"""Minimal OpenAI-Realtime-compatible client for speech-to-speech.

Usage:
    python listen_and_play_realtime.py --host 127.0.0.1 --port 8765
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import signal
import sys

try:
    import websockets
except ImportError:
    sys.exit("websockets package missing. Run: pip install websockets")

DEFAULT_HOST = os.getenv("S2S_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.getenv("S2S_PORT", "8765"))

SAMPLE_RATE = 24000
CHANNELS = 1
CHUNK_MS = 60


def build_session_update() -> dict:
    return {
        "type": "session.update",
        "session": {
            "type": "realtime",
            "instructions": (
                "You are a concise, friendly voice assistant. "
                "Keep replies short and natural for speech."
            ),
            "audio": {
                "input": {
                    "turn_detection": {
                        "type": "server_vad",
                        "interrupt_response": True,
                    }
                },
                "output": {
                    "voice": "alloy",
                },
            },
        },
    }


async def run(host: str, port: int) -> None:
    url = f"ws://{host}:{port}/v1/realtime"
    print(f"[client] connecting -> {url}")

    async with websockets.connect(url, max_size=16 * 1024 * 1024) as ws:
        print("[client] connected")

        # Send session config
        await ws.send(json.dumps(build_session_update()))
        print("[client] session.update sent")

        speaker = await _pick_speaker()
        if speaker:
            await ws.send(json.dumps({
                "type": "session.update",
                "session": {"audio": {"output": {"voice": speaker}}}
            }))
            print(f"[client] voice set -> {speaker}")

        await asyncio.gather(_receive(ws), _send_events(ws))


async def _receive(ws) -> None:
    async for raw in ws:
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        etype = event.get("type", "")
        if etype in ("response.audio.delta",):
            pass
        elif etype in ("session.created", "session.updated", "response.created",
                       "response.done", "response.audio.done",
                       "conversation.item.input_audio_transcription.completed",
                       "conversation.item.input_audio_transcription.partial"):
            print(f"[server] {etype} :: {json.dumps({k: event.get(k) for k in event if k not in ('delta', 'transcript', 'audio')})[:220]}")
        else:
            preview = json.dumps(event)
            print(f"[server] {etype} :: {preview[:180]}")


async def _send_events(ws) -> None:
    loop = asyncio.get_event_loop()
    while True:
        await asyncio.sleep(0.5)


async def _pick_speaker() -> str | None:
    # Attempt to read any local speaker prefs in future; default None = unchanged.
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="S2S minimal client")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    try:
        asyncio.run(run(args.host, args.port))
    except KeyboardInterrupt:
        print("\n[client] stopped")


if __name__ == "__main__":
    main()
