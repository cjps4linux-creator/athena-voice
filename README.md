# Athena Voice

**Real-time speech-to-speech voice agent  -  WebSocket client for OpenAI Realtime-compatible backends.**

Built by Conrad CJ Wilson as part of the Hermes AI ecosystem. Demonstrates WebSocket-based voice orchestration: 24 kHz audio streaming, server-side VAD, interrupt-response handling, and OpenAI Realtime API compatibility.

## What It Does

| Feature | Detail |
|---|---|
| WebSocket client | Full-duplex audio streaming to `/v1/realtime` endpoints |
| Audio format | 24 kHz, mono, 16-bit PCM |
| VAD | Server-side voice activity detection |
| Barge-in | User speech cancels active TTS mid-utterance |
| Interrupt handling | Graceful response to speech interruptions |
| Backend compatibility | OpenAI Realtime API, LocateAnything-3B, any compatible server |

## Architecture

```
User (mic/speaker)
    │
    ▼
WebSocket Client (this repo)
    │
    ├──► Audio input  → 24 kHz PCM chunks
    ├──► Server-side VAD
    ├──► LLM / reasoning backend
    └──◄── Audio output ← TTS stream
```

## Quick Start

```bash
# Clone
git clone https://github.com/cjps4linux-creator/athena-voice.git
cd athena-voice

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your OPENROUTER_API_KEY or backend URL

# Run
python listen_and_play_realtime.py --host 127.0.0.1 --port 8765
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | *(required)* | API key for the Realtime backend |
| `S2S_HOST` | `127.0.0.1` | WebSocket server host |
| `S2S_PORT` | `8765` | WebSocket server port |

## GUI

Open `gui/index.html` in a browser for the visual interface. The GUI connects to the running WebSocket server and provides real-time audio visualization.

## Requirements

- Python 3.10+
- `websockets` ≥ 12.0
- `numpy` ≥ 1.24.0
- Compatible backend server (OpenAI Realtime API, LocateAnything-3B, etc.)

## Security

- **Never commit `.env`**  -  it contains API keys
- Use `.env.example` as a template with [content pending] values
- API keys are loaded from environment variables only
- Default host binds to `127.0.0.1` (localhost only)

## License

MIT  -  see [LICENSE](LICENSE)

## Author

Conrad CJ Wilson  -  [@cjps4linux-creator](https://github.com/cjps4linux-creator)
