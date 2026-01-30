# JARVIS AI Assistant: Complete Project Specification
## A Comprehensive Guide to Building a Personal AI Assistant (January 2026)

---

## Executive Summary

This document provides a complete A-to-Z specification for building a JARVIS-like personal AI assistant. It covers architecture, technology choices, implementation details, deployment strategies, security considerations, and maintenance procedures. This specification is designed to be handed to a development team or freelance developer for implementation.

**Project Goal:** Create a voice-activated, multi-modal AI assistant capable of natural conversation, smart home control, information retrieval, task automation, and proactive assistance—all while maintaining privacy and running with minimal latency.

**Estimated Development Timeline:** 16-24 weeks for MVP, 32-48 weeks for full feature set
**Estimated Budget Range:** $15,000-$50,000 (development) + ongoing infrastructure costs

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Core Architecture](#2-core-architecture)
3. [Voice Interface Layer](#3-voice-interface-layer)
4. [Brain Layer (LLM Orchestration)](#4-brain-layer-llm-orchestration)
5. [Smart Home Integration](#5-smart-home-integration)
6. [Computer Vision Module](#6-computer-vision-module)
7. [Memory & Context System](#7-memory--context-system)
8. [Tool & API Integration](#8-tool--api-integration)
9. [User Interface Options](#9-user-interface-options)
10. [Security & Privacy](#10-security--privacy)
11. [Infrastructure & Deployment](#11-infrastructure--deployment)
12. [Development Phases](#12-development-phases)
13. [Testing Strategy](#13-testing-strategy)
14. [Maintenance & Updates](#14-maintenance--updates)
15. [Budget & Resource Estimates](#15-budget--resource-estimates)
16. [Technical Appendices](#16-technical-appendices)

---

## 1. System Overview

### 1.1 What JARVIS Does (Feature Matrix)

| Category | Feature | Priority | Complexity |
|----------|---------|----------|------------|
| **Voice** | Wake word detection ("Hey JARVIS") | P0 | Medium |
| **Voice** | Real-time speech recognition | P0 | Medium |
| **Voice** | Natural text-to-speech response | P0 | Medium |
| **Voice** | Interruption handling | P1 | High |
| **Voice** | Multi-language support | P2 | Medium |
| **Conversation** | Context-aware multi-turn dialogue | P0 | High |
| **Conversation** | Personality customization | P1 | Low |
| **Conversation** | Proactive suggestions | P2 | High |
| **Smart Home** | Light control | P0 | Low |
| **Smart Home** | Thermostat control | P1 | Low |
| **Smart Home** | Security system integration | P1 | Medium |
| **Smart Home** | Device status queries | P0 | Low |
| **Smart Home** | Automation triggers | P1 | Medium |
| **Information** | Web search & research | P0 | Medium |
| **Information** | Weather & news briefings | P0 | Low |
| **Information** | Calendar & schedule management | P0 | Medium |
| **Information** | Email reading & drafting | P1 | Medium |
| **Tasks** | Reminders & timers | P0 | Low |
| **Tasks** | Note-taking & lists | P0 | Low |
| **Tasks** | Document creation | P2 | High |
| **Vision** | Person recognition | P2 | High |
| **Vision** | Object detection | P2 | High |
| **Vision** | Screen content analysis | P3 | High |

### 1.2 Design Principles

1. **Privacy-First**: Maximum local processing, encrypted data, user owns all data
2. **Low Latency**: Voice-to-response under 500ms for conversational flow
3. **Modular Architecture**: Each component independently upgradeable
4. **Graceful Degradation**: Works offline with reduced features
5. **Extensibility**: Plugin system for adding new capabilities
6. **Natural Interaction**: Feels like talking to a knowledgeable assistant, not a robot

### 1.3 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Voice UI   │  │   Web UI     │  │  Mobile App  │  │  Desktop App │     │
│  │  (Speakers/  │  │  (Dashboard) │  │  (iOS/And)   │  │  (Electron)  │     │
│  │   Mics)      │  │              │  │              │  │              │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼────────────────┼────────────────┼────────────────┼────────────────┘
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           VOICE INTERFACE LAYER                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Wake Word      │  │  Speech-to-Text │  │  Text-to-Speech │              │
│  │  Detection      │  │  (STT)          │  │  (TTS)          │              │
│  │  (Porcupine/    │  │  (Whisper/      │  │  (Inworld/      │              │
│  │   OpenWakeWord) │  │   Deepgram)     │  │   ElevenLabs)   │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BRAIN LAYER                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    AGENT ORCHESTRATOR (LangGraph)                    │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │    │
│  │  │  Supervisor │  │  Router     │  │  Memory     │  │  Tool      │  │    │
│  │  │  Agent      │  │  Agent      │  │  Agent      │  │  Executor  │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         LLM BACKENDS                                 │    │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐            │    │
│  │  │ Cloud LLMs    │  │ Local LLMs    │  │ Realtime API  │            │    │
│  │  │ (Claude/GPT)  │  │ (Ollama)      │  │ (OpenAI)      │            │    │
│  │  └───────────────┘  └───────────────┘  └───────────────┘            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          INTEGRATION LAYER                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Smart Home  │  │  Calendar/   │  │  Web Search  │  │  Computer    │     │
│  │  (Home Asst) │  │  Email APIs  │  │  & Research  │  │  Vision      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             DATA LAYER                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Vector DB   │  │  SQLite/     │  │  Redis       │  │  File        │     │
│  │  (ChromaDB)  │  │  PostgreSQL  │  │  (Cache)     │  │  Storage     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Architecture

### 2.1 Technology Stack Overview

| Layer | Component | Recommended Technology | Alternatives |
|-------|-----------|----------------------|--------------|
| **Runtime** | Backend Server | Python 3.11+ with FastAPI | Node.js with Express |
| **Voice Transport** | Real-time Communication | LiveKit | Vapi, Daily.co |
| **STT** | Speech Recognition | Deepgram Nova-3 (cloud) / Whisper (local) | AssemblyAI, Azure Speech |
| **TTS** | Speech Synthesis | Inworld TTS-1.5 Max / ElevenLabs | OpenAI TTS, Cartesia |
| **Wake Word** | Activation Detection | Porcupine (Picovoice) | OpenWakeWord (open source) |
| **LLM Orchestration** | Agent Framework | LangGraph + LangChain | AutoGen, CrewAI |
| **Primary LLM** | Cloud Intelligence | Claude Sonnet 4.5 / GPT-4.1 | Gemini 2.0, Mistral Large |
| **Local LLM** | Offline/Privacy | Ollama with Llama 3.3 70B | vLLM, llama.cpp |
| **Smart Home** | Home Automation | Home Assistant | openHAB, Hubitat |
| **Protocol** | Device Communication | Matter + Thread | Zigbee, Z-Wave |
| **Computer Vision** | Object Detection | YOLO26 / YOLOv8 | RF-DETR |
| **Face Recognition** | Person Identification | DeepFace / FaceNet | InsightFace |
| **Vector Database** | Memory/RAG | ChromaDB | Pinecone, Weaviate, Qdrant |
| **Relational Database** | Structured Data | PostgreSQL / SQLite | MySQL |
| **Cache** | Session/Fast Access | Redis | Memcached |
| **Message Queue** | Async Tasks | Redis Streams / Celery | RabbitMQ |
| **Containerization** | Deployment | Docker + Docker Compose | Kubernetes |

### 2.2 Communication Protocols

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMMUNICATION FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Client ←──WebRTC──→ LiveKit Server ←──WebSocket──→ JARVIS Core │
│                                                                  │
│  JARVIS Core ←──REST/gRPC──→ Smart Home (Home Assistant)        │
│                                                                  │
│  JARVIS Core ←──HTTP──→ External APIs (Weather, Calendar, etc)  │
│                                                                  │
│  JARVIS Core ←──WebSocket──→ LLM APIs (OpenAI Realtime)         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Protocol Selection Rationale:**
- **WebRTC** for voice: Handles packet loss gracefully, low latency (~50ms), works across network conditions
- **WebSocket** for LLM streaming: Persistent connection for token-by-token responses
- **REST** for integrations: Stateless, cacheable, well-supported
- **Matter/Thread** for IoT: Industry standard, local-first, multi-vendor compatible

### 2.3 Latency Budget

| Stage | Target | Maximum |
|-------|--------|---------|
| Wake word detection | 50ms | 100ms |
| Audio capture to STT start | 50ms | 100ms |
| STT processing | 150ms | 300ms |
| LLM first token | 200ms | 500ms |
| TTS first audio chunk | 100ms | 200ms |
| **Total voice-to-voice** | **550ms** | **1200ms** |

---

## 3. Voice Interface Layer

### 3.1 Wake Word Detection

**Recommended: Porcupine by Picovoice**

```python
# Installation
pip install pvporcupine

# Implementation
import pvporcupine
import pyaudio
import struct

class WakeWordDetector:
    def __init__(self, access_key: str, wake_word: str = "jarvis"):
        self.porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=[wake_word]  # Custom wake word requires training
        )
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )
    
    def listen(self) -> bool:
        """Continuously listen for wake word, returns True when detected."""
        pcm = self.stream.read(self.porcupine.frame_length)
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
        keyword_index = self.porcupine.process(pcm)
        return keyword_index >= 0
```

**Alternative: OpenWakeWord (Open Source)**
```python
pip install openwakeword
```

**Custom Wake Word Training:**
- Porcupine: Use Picovoice Console (https://console.picovoice.ai)
- Requires 3-5 recordings of wake word
- Outputs .ppn file for deployment

### 3.2 Speech-to-Text (STT)

**Primary: Deepgram Nova-3 (Cloud)**

```python
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

class RealtimeSTT:
    def __init__(self, api_key: str):
        self.client = DeepgramClient(api_key)
        self.connection = None
        self.transcript = ""
        
    async def start_streaming(self, on_transcript: callable):
        options = LiveOptions(
            model="nova-3",
            language="en-US",
            smart_format=True,
            encoding="linear16",
            sample_rate=16000,
            channels=1,
            interim_results=True,
            utterance_end_ms=1000,
            vad_events=True,
        )
        
        self.connection = self.client.listen.live.v("1")
        
        @self.connection.on(LiveTranscriptionEvents.Transcript)
        async def on_message(result):
            transcript = result.channel.alternatives[0].transcript
            if result.is_final:
                await on_transcript(transcript)
        
        await self.connection.start(options)
    
    async def send_audio(self, audio_chunk: bytes):
        await self.connection.send(audio_chunk)
```

**Fallback: Local Whisper (via Faster-Whisper)**

```python
from faster_whisper import WhisperModel

class LocalSTT:
    def __init__(self, model_size: str = "large-v3"):
        self.model = WhisperModel(
            model_size,
            device="cuda",  # or "cpu"
            compute_type="float16"  # or "int8" for CPU
        )
    
    def transcribe(self, audio_path: str) -> str:
        segments, info = self.model.transcribe(
            audio_path,
            beam_size=5,
            language="en",
            vad_filter=True
        )
        return " ".join([segment.text for segment in segments])
```

**STT Provider Comparison (January 2026):**

| Provider | Accuracy (WER) | Latency | Cost | Best For |
|----------|----------------|---------|------|----------|
| Deepgram Nova-3 | 8.4% | ~300ms | $0.0043/min | Production real-time |
| AssemblyAI Universal | 7.9% | ~300ms | $0.006/min | High accuracy needs |
| OpenAI Whisper (API) | 9.2% | ~500ms | $0.006/min | OpenAI ecosystem |
| Whisper (local) | 9.2% | ~200ms (GPU) | Free | Privacy/offline |
| Google Cloud STT | 11.3% | ~400ms | $0.006/min | Google ecosystem |

### 3.3 Text-to-Speech (TTS)

**Primary: Inworld TTS-1.5 Max (Recommended for Quality)**

```python
import httpx

class InworldTTS:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.inworld.ai/v1/tts"
    
    async def synthesize_streaming(
        self, 
        text: str, 
        voice: str = "echo",
        on_audio_chunk: callable = None
    ):
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/synthesize",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "text": text,
                    "voice": voice,
                    "output_format": "mp3",
                    "streaming": True
                }
            ) as response:
                async for chunk in response.aiter_bytes():
                    if on_audio_chunk:
                        await on_audio_chunk(chunk)
```

**Alternative: ElevenLabs (Best Voice Cloning)**

```python
from elevenlabs import generate, stream, set_api_key

set_api_key("your-api-key")

def speak_streaming(text: str, voice: str = "Adam"):
    audio_stream = generate(
        text=text,
        voice=voice,
        model="eleven_turbo_v2_5",
        stream=True
    )
    stream(audio_stream)
```

**TTS Provider Comparison (January 2026):**

| Provider | Quality | Latency (First Chunk) | Cost | Best For |
|----------|---------|----------------------|------|----------|
| Inworld TTS-1.5 Max | #1 Ranked | ~200ms | $7/1M chars | Production quality |
| Inworld TTS-1.5 Mini | Excellent | <100ms | $5/1M chars | Ultra-low latency |
| ElevenLabs | Excellent | ~300ms | $11/1M chars | Voice cloning |
| OpenAI TTS | Very Good | ~250ms | $15/1M chars | OpenAI ecosystem |
| Cartesia Sonic-2 | Very Good | ~150ms | $8/1M chars | Speed-focused |

### 3.4 Real-Time Voice Pipeline (LiveKit Integration)

```python
from livekit.agents import (
    Agent, AgentSession, JobContext, cli
)
from livekit.plugins import silero, deepgram, openai as openai_plugin

class JARVISVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="""You are JARVIS, an advanced AI assistant.
            Be helpful, concise, and occasionally witty.
            Address the user as 'sir' or 'ma'am' unless told otherwise."""
        )
    
    async def on_user_speech(self, transcript: str):
        # Process user speech and generate response
        response = await self.process_query(transcript)
        await self.speak(response)

async def entrypoint(ctx: JobContext):
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-3"),
        llm=openai_plugin.LLM(model="gpt-4.1"),
        tts=openai_plugin.TTS(voice="echo"),
    )
    
    await session.start(
        agent=JARVISVoiceAgent(),
        room=ctx.room
    )

if __name__ == "__main__":
    cli.run_app(entrypoint)
```

### 3.5 Voice Activity Detection (VAD)

```python
# Silero VAD - Industry standard for voice detection
from livekit.plugins import silero

vad = silero.VAD.load(
    min_speech_duration=0.1,  # Minimum speech duration to trigger
    min_silence_duration=0.5,  # Silence duration to end utterance
    padding_duration=0.1,      # Padding around detected speech
    sample_rate=16000,
    activation_threshold=0.5
)
```

---

## 4. Brain Layer (LLM Orchestration)

### 4.1 Agent Architecture with LangGraph

```python
from typing import Annotated, Literal, TypedDict
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

# Define the state
class JARVISState(TypedDict):
    messages: list
    user_context: dict
    active_tools: list
    current_intent: str

# Initialize the LLM
llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    temperature=0.7,
    max_tokens=4096
)

# Define the supervisor agent
def supervisor_agent(state: JARVISState):
    """Routes requests to appropriate specialized agents."""
    system_prompt = """You are JARVIS's supervisor. Analyze the user request and route to:
    - 'smart_home' for device control
    - 'information' for questions, search, research
    - 'tasks' for reminders, calendar, lists
    - 'conversation' for general chat
    - 'END' if task is complete
    
    Respond with JSON: {"next": "agent_name", "reason": "brief explanation"}
    """
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    
    # Parse routing decision
    routing = parse_routing(response.content)
    state["current_intent"] = routing["next"]
    
    return state

# Define specialized agents
def smart_home_agent(state: JARVISState):
    """Handles smart home device control."""
    system_prompt = """You are JARVIS's smart home controller. You can:
    - Control lights (on/off, brightness, color)
    - Adjust thermostats
    - Lock/unlock doors
    - Check device status
    
    Use available tools to execute commands. Be concise in responses.
    """
    # Implementation with Home Assistant tools
    pass

def information_agent(state: JARVISState):
    """Handles information retrieval and research."""
    system_prompt = """You are JARVIS's research assistant. You can:
    - Search the web for current information
    - Retrieve weather forecasts
    - Look up facts and data
    - Summarize documents
    
    Provide accurate, sourced information.
    """
    # Implementation with search and RAG tools
    pass

def tasks_agent(state: JARVISState):
    """Handles task management."""
    system_prompt = """You are JARVIS's task manager. You can:
    - Set reminders and alarms
    - Manage calendar events
    - Create and update lists
    - Track deadlines
    
    Confirm actions taken and provide relevant details.
    """
    # Implementation with calendar and reminder tools
    pass

def conversation_agent(state: JARVISState):
    """Handles general conversation."""
    system_prompt = """You are JARVIS, an AI assistant with the personality of
    Tony Stark's AI from Iron Man. Be:
    - Helpful and knowledgeable
    - Occasionally witty with dry humor
    - Professional but personable
    - Concise (voice responses should be brief)
    """
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    state["messages"].append(response)
    return state

# Build the graph
def build_jarvis_graph():
    workflow = StateGraph(JARVISState)
    
    # Add nodes
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("smart_home", smart_home_agent)
    workflow.add_node("information", information_agent)
    workflow.add_node("tasks", tasks_agent)
    workflow.add_node("conversation", conversation_agent)
    
    # Define edges
    workflow.add_edge(START, "supervisor")
    
    # Conditional routing from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        lambda state: state["current_intent"],
        {
            "smart_home": "smart_home",
            "information": "information",
            "tasks": "tasks",
            "conversation": "conversation",
            "END": END
        }
    )
    
    # All agents can loop back or end
    for agent in ["smart_home", "information", "tasks", "conversation"]:
        workflow.add_edge(agent, "supervisor")
    
    return workflow.compile()

# Usage
jarvis = build_jarvis_graph()

async def process_request(user_message: str, context: dict = None):
    initial_state = {
        "messages": [HumanMessage(content=user_message)],
        "user_context": context or {},
        "active_tools": [],
        "current_intent": ""
    }
    
    result = await jarvis.ainvoke(initial_state)
    return result["messages"][-1].content
```

### 4.2 LLM Selection Strategy

```python
class LLMRouter:
    """Routes requests to appropriate LLM based on task requirements."""
    
    def __init__(self):
        # Cloud LLMs for complex reasoning
        self.claude = ChatAnthropic(model="claude-sonnet-4-5-20250929")
        self.gpt4 = ChatOpenAI(model="gpt-4.1")
        
        # Local LLM for privacy-sensitive or offline
        self.local = ChatOllama(model="llama3.3:70b")
        
        # Realtime API for ultra-low latency voice
        self.realtime = OpenAIRealtime(model="gpt-realtime-2025-08-28")
    
    def select_llm(self, request_type: str, privacy_level: str):
        """Select appropriate LLM based on request characteristics."""
        
        if privacy_level == "maximum":
            # Sensitive data - use local only
            return self.local
        
        if request_type == "voice_conversation":
            # Real-time voice - use OpenAI Realtime API
            return self.realtime
        
        if request_type in ["complex_reasoning", "code_generation"]:
            # Complex tasks - use Claude
            return self.claude
        
        if request_type == "general":
            # General queries - use GPT-4
            return self.gpt4
        
        # Default fallback
        return self.gpt4
```

### 4.3 Local LLM Setup with Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended models
ollama pull llama3.3:70b      # Best quality local model
ollama pull llama3.2:3b       # Fast, small model for simple tasks
ollama pull nomic-embed-text  # For embeddings/RAG

# Start Ollama server
ollama serve
```

```python
# Integration with LangChain
from langchain_ollama import ChatOllama

local_llm = ChatOllama(
    model="llama3.3:70b",
    base_url="http://localhost:11434",
    temperature=0.7,
    num_ctx=8192,  # Context window
    num_gpu=1,     # GPU layers
)

# Use for privacy-sensitive queries
response = local_llm.invoke("What appointments do I have today?")
```

### 4.4 OpenAI Realtime API Integration

```python
from livekit.plugins import openai

class RealtimeVoiceAgent:
    """Uses OpenAI's native speech-to-speech for minimum latency."""
    
    def __init__(self):
        self.model = openai.realtime.RealtimeModel(
            model="gpt-realtime-2025-08-28",
            voice="echo",
            temperature=0.8,
            turn_detection={
                "type": "server_vad",
                "threshold": 0.5,
                "prefix_padding_ms": 300,
                "silence_duration_ms": 500
            }
        )
    
    async def create_session(self, instructions: str):
        """Create a new realtime session."""
        session = await self.model.create_session(
            instructions=instructions,
            tools=self.get_available_tools()
        )
        return session
    
    def get_available_tools(self):
        return [
            {
                "name": "control_lights",
                "description": "Control smart lights",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room": {"type": "string"},
                        "action": {"type": "string", "enum": ["on", "off", "dim"]}
                    }
                }
            },
            # ... more tools
        ]
```

---

## 5. Smart Home Integration

### 5.1 Home Assistant Setup

**Installation (Docker Recommended):**

```yaml
# docker-compose.yml
version: '3.8'
services:
  homeassistant:
    container_name: homeassistant
    image: ghcr.io/home-assistant/home-assistant:stable
    volumes:
      - ./config:/config
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
    privileged: true
    network_mode: host
    
  matter-server:
    container_name: matter-server
    image: ghcr.io/home-assistant-libs/python-matter-server:stable
    restart: unless-stopped
    security_opt:
      - apparmor:unconfined
    volumes:
      - ./matter:/data
    ports:
      - "5580:5580"
```

### 5.2 Home Assistant API Integration

```python
import aiohttp
from typing import Optional, Dict, Any

class HomeAssistantClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    async def call_service(
        self, 
        domain: str, 
        service: str, 
        entity_id: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """Call a Home Assistant service."""
        url = f"{self.base_url}/api/services/{domain}/{service}"
        payload = {"entity_id": entity_id}
        if data:
            payload.update(data)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as resp:
                return await resp.json()
    
    async def get_state(self, entity_id: str) -> Dict[str, Any]:
        """Get the state of an entity."""
        url = f"{self.base_url}/api/states/{entity_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                return await resp.json()
    
    # Convenience methods
    async def turn_on_light(self, entity_id: str, brightness: int = 255):
        return await self.call_service(
            "light", "turn_on", entity_id,
            {"brightness": brightness}
        )
    
    async def turn_off_light(self, entity_id: str):
        return await self.call_service("light", "turn_off", entity_id)
    
    async def set_thermostat(self, entity_id: str, temperature: float):
        return await self.call_service(
            "climate", "set_temperature", entity_id,
            {"temperature": temperature}
        )
    
    async def lock_door(self, entity_id: str):
        return await self.call_service("lock", "lock", entity_id)
    
    async def get_all_devices(self) -> list:
        """Get all devices/entities."""
        url = f"{self.base_url}/api/states"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                return await resp.json()
```

### 5.3 Smart Home Tools for LLM

```python
from langchain.tools import tool
from pydantic import BaseModel, Field

class LightControlInput(BaseModel):
    room: str = Field(description="The room name (e.g., 'living room', 'bedroom')")
    action: str = Field(description="Action to perform: 'on', 'off', or 'dim'")
    brightness: int = Field(default=100, description="Brightness level 0-100 (for 'dim' action)")

@tool("control_lights", args_schema=LightControlInput)
async def control_lights(room: str, action: str, brightness: int = 100) -> str:
    """Control smart lights in a specific room."""
    
    ha_client = HomeAssistantClient(
        base_url="http://homeassistant.local:8123",
        token=os.getenv("HA_TOKEN")
    )
    
    # Map room names to entity IDs
    room_mapping = {
        "living room": "light.living_room_main",
        "bedroom": "light.bedroom_main",
        "kitchen": "light.kitchen_main",
        # ... more mappings
    }
    
    entity_id = room_mapping.get(room.lower())
    if not entity_id:
        return f"Unknown room: {room}. Available rooms: {', '.join(room_mapping.keys())}"
    
    if action == "on":
        await ha_client.turn_on_light(entity_id, int(brightness * 2.55))
        return f"Turned on lights in {room} at {brightness}% brightness."
    elif action == "off":
        await ha_client.turn_off_light(entity_id)
        return f"Turned off lights in {room}."
    elif action == "dim":
        await ha_client.turn_on_light(entity_id, int(brightness * 2.55))
        return f"Dimmed lights in {room} to {brightness}%."
    else:
        return f"Unknown action: {action}. Use 'on', 'off', or 'dim'."

class ThermostatInput(BaseModel):
    temperature: float = Field(description="Target temperature in Fahrenheit")
    zone: str = Field(default="main", description="Climate zone name")

@tool("set_thermostat", args_schema=ThermostatInput)
async def set_thermostat(temperature: float, zone: str = "main") -> str:
    """Set the thermostat to a specific temperature."""
    
    ha_client = HomeAssistantClient(
        base_url="http://homeassistant.local:8123",
        token=os.getenv("HA_TOKEN")
    )
    
    zone_mapping = {
        "main": "climate.main_thermostat",
        "upstairs": "climate.upstairs_thermostat",
    }
    
    entity_id = zone_mapping.get(zone.lower())
    if not entity_id:
        return f"Unknown zone: {zone}"
    
    await ha_client.set_thermostat(entity_id, temperature)
    return f"Set {zone} thermostat to {temperature}°F."

@tool("get_home_status")
async def get_home_status() -> str:
    """Get the current status of all smart home devices."""
    
    ha_client = HomeAssistantClient(
        base_url="http://homeassistant.local:8123",
        token=os.getenv("HA_TOKEN")
    )
    
    devices = await ha_client.get_all_devices()
    
    # Organize by domain
    status = {
        "lights": [],
        "climate": [],
        "locks": [],
        "sensors": []
    }
    
    for device in devices:
        entity_id = device["entity_id"]
        domain = entity_id.split(".")[0]
        
        if domain == "light":
            status["lights"].append({
                "name": device["attributes"].get("friendly_name", entity_id),
                "state": device["state"],
                "brightness": device["attributes"].get("brightness", "N/A")
            })
        elif domain == "climate":
            status["climate"].append({
                "name": device["attributes"].get("friendly_name", entity_id),
                "current_temp": device["attributes"].get("current_temperature"),
                "target_temp": device["attributes"].get("temperature"),
                "mode": device["state"]
            })
        # ... more domains
    
    return json.dumps(status, indent=2)
```

### 5.4 Matter Protocol Integration

```yaml
# Home Assistant configuration.yaml
matter:
  adapter: chip
  storage_path: /config/matter
```

```python
# Commissioning new Matter devices programmatically
async def commission_matter_device(qr_code: str):
    """Add a new Matter device using QR code."""
    
    # Use Home Assistant's Matter integration
    ha_client = HomeAssistantClient(...)
    
    await ha_client.call_service(
        "matter",
        "commission_with_code",
        None,
        {"code": qr_code}
    )
```

---

## 6. Computer Vision Module

### 6.1 Object Detection with YOLO26

```python
from ultralytics import YOLO
import cv2
import numpy as np

class VisionModule:
    def __init__(self, model_size: str = "yolo26m.pt"):
        # Load YOLO26 model
        self.detector = YOLO(model_size)
        
        # Load face recognition model
        from deepface import DeepFace
        self.face_model = DeepFace
    
    def detect_objects(self, frame: np.ndarray) -> list:
        """Detect objects in a frame."""
        results = self.detector(frame, conf=0.5)
        
        detections = []
        for result in results:
            for box in result.boxes:
                detections.append({
                    "class": result.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy[0].tolist()
                })
        
        return detections
    
    def detect_and_recognize_faces(
        self, 
        frame: np.ndarray, 
        known_faces_db: str = "faces/"
    ) -> list:
        """Detect faces and attempt to recognize them."""
        
        try:
            # DeepFace handles detection and recognition
            results = self.face_model.find(
                img_path=frame,
                db_path=known_faces_db,
                model_name="VGG-Face",
                enforce_detection=False
            )
            
            recognized = []
            for result in results:
                if not result.empty:
                    recognized.append({
                        "identity": result.iloc[0]["identity"],
                        "distance": float(result.iloc[0]["distance"]),
                        "verified": result.iloc[0]["distance"] < 0.4
                    })
            
            return recognized
            
        except Exception as e:
            return [{"error": str(e)}]
    
    def analyze_scene(self, frame: np.ndarray) -> dict:
        """Comprehensive scene analysis."""
        
        # Object detection
        objects = self.detect_objects(frame)
        
        # Face recognition
        faces = self.detect_and_recognize_faces(frame)
        
        # Scene understanding (using vision-language model)
        scene_description = self.describe_scene(frame)
        
        return {
            "objects": objects,
            "faces": faces,
            "description": scene_description,
            "timestamp": datetime.now().isoformat()
        }
    
    def describe_scene(self, frame: np.ndarray) -> str:
        """Use vision-language model to describe the scene."""
        
        # Encode image for API
        _, buffer = cv2.imencode('.jpg', frame)
        image_base64 = base64.b64encode(buffer).decode()
        
        # Use Claude or GPT-4 Vision
        from anthropic import Anthropic
        client = Anthropic()
        
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": "Briefly describe what you see in this image. Focus on people, activities, and notable objects."
                    }
                ]
            }]
        )
        
        return response.content[0].text
```

### 6.2 Camera Integration

```python
import cv2
from typing import Generator
import threading
import queue

class CameraManager:
    def __init__(self):
        self.cameras = {}
        self.frame_queues = {}
        self.running = False
    
    def add_camera(self, name: str, source: int | str):
        """Add a camera source (device index or RTSP URL)."""
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            raise ValueError(f"Cannot open camera: {source}")
        
        self.cameras[name] = cap
        self.frame_queues[name] = queue.Queue(maxsize=10)
    
    def start_capture(self):
        """Start capturing frames from all cameras."""
        self.running = True
        
        for name, cap in self.cameras.items():
            thread = threading.Thread(
                target=self._capture_loop,
                args=(name, cap)
            )
            thread.daemon = True
            thread.start()
    
    def _capture_loop(self, name: str, cap: cv2.VideoCapture):
        """Continuous capture loop for a camera."""
        while self.running:
            ret, frame = cap.read()
            if ret:
                # Drop old frames if queue is full
                if self.frame_queues[name].full():
                    try:
                        self.frame_queues[name].get_nowait()
                    except queue.Empty:
                        pass
                
                self.frame_queues[name].put(frame)
    
    def get_frame(self, camera_name: str) -> np.ndarray | None:
        """Get the latest frame from a camera."""
        try:
            return self.frame_queues[camera_name].get_nowait()
        except queue.Empty:
            return None
    
    def stop(self):
        """Stop all capture threads."""
        self.running = False
        for cap in self.cameras.values():
            cap.release()
```

### 6.3 Vision Tools for LLM

```python
@tool("analyze_camera")
async def analyze_camera(camera_name: str = "front_door") -> str:
    """Analyze what a security camera sees."""
    
    vision = VisionModule()
    camera_manager = CameraManager()
    
    frame = camera_manager.get_frame(camera_name)
    if frame is None:
        return f"No frame available from camera: {camera_name}"
    
    analysis = vision.analyze_scene(frame)
    
    # Format for voice response
    response_parts = []
    
    if analysis["faces"]:
        names = [f["identity"].split("/")[-1] for f in analysis["faces"] if f.get("verified")]
        if names:
            response_parts.append(f"I see {', '.join(names)}")
    
    if analysis["objects"]:
        object_counts = {}
        for obj in analysis["objects"]:
            obj_class = obj["class"]
            object_counts[obj_class] = object_counts.get(obj_class, 0) + 1
        
        objects_str = ", ".join([
            f"{count} {name}{'s' if count > 1 else ''}"
            for name, count in object_counts.items()
        ])
        response_parts.append(f"Objects detected: {objects_str}")
    
    response_parts.append(f"Scene: {analysis['description']}")
    
    return ". ".join(response_parts)

@tool("who_is_at_door")
async def who_is_at_door() -> str:
    """Check who is at the front door using the doorbell camera."""
    return await analyze_camera("front_door")
```

---

## 7. Memory & Context System

### 7.1 Vector Database Setup (ChromaDB)

```python
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import OllamaEmbeddings

class MemorySystem:
    def __init__(self, persist_directory: str = "./jarvis_memory"):
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embeddings model (local for privacy)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # Create collections for different memory types
        self.conversations = self.client.get_or_create_collection(
            name="conversations",
            metadata={"description": "Conversation history"}
        )
        
        self.user_preferences = self.client.get_or_create_collection(
            name="user_preferences",
            metadata={"description": "User preferences and patterns"}
        )
        
        self.knowledge = self.client.get_or_create_collection(
            name="knowledge",
            metadata={"description": "Learned facts and information"}
        )
    
    async def store_conversation(
        self, 
        user_message: str, 
        assistant_response: str,
        metadata: dict = None
    ):
        """Store a conversation exchange."""
        
        combined_text = f"User: {user_message}\nAssistant: {assistant_response}"
        embedding = await self.embeddings.aembed_query(combined_text)
        
        self.conversations.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            documents=[combined_text],
            metadatas=[{
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "assistant_response": assistant_response,
                **(metadata or {})
            }]
        )
    
    async def recall_relevant_context(
        self, 
        query: str, 
        n_results: int = 5
    ) -> list:
        """Retrieve relevant past conversations."""
        
        query_embedding = await self.embeddings.aembed_query(query)
        
        results = self.conversations.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return [
            {
                "content": doc,
                "metadata": meta,
                "relevance": 1 - dist  # Convert distance to similarity
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
    
    async def learn_preference(self, preference_type: str, value: str):
        """Store a user preference."""
        
        text = f"{preference_type}: {value}"
        embedding = await self.embeddings.aembed_query(text)
        
        # Check if preference already exists
        existing = self.user_preferences.query(
            query_embeddings=[embedding],
            n_results=1,
            where={"type": preference_type}
        )
        
        if existing["ids"][0]:
            # Update existing
            self.user_preferences.update(
                ids=existing["ids"][0],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{
                    "type": preference_type,
                    "value": value,
                    "updated_at": datetime.now().isoformat()
                }]
            )
        else:
            # Add new
            self.user_preferences.add(
                ids=[str(uuid.uuid4())],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{
                    "type": preference_type,
                    "value": value,
                    "created_at": datetime.now().isoformat()
                }]
            )
    
    async def get_user_context(self) -> dict:
        """Build a context object from user preferences."""
        
        all_prefs = self.user_preferences.get()
        
        context = {}
        for meta in all_prefs["metadatas"]:
            context[meta["type"]] = meta["value"]
        
        return context
```

### 7.2 Short-Term Memory (Session Context)

```python
from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ConversationTurn:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

class SessionMemory:
    """Manages short-term memory for a conversation session."""
    
    def __init__(self, max_turns: int = 20, max_tokens: int = 8000):
        self.turns: deque[ConversationTurn] = deque(maxlen=max_turns)
        self.max_tokens = max_tokens
        self.context: dict = {}  # Session-specific context
    
    def add_turn(self, role: str, content: str, metadata: dict = None):
        """Add a conversation turn."""
        turn = ConversationTurn(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.turns.append(turn)
    
    def get_messages_for_llm(self) -> List[dict]:
        """Get messages formatted for LLM API."""
        messages = []
        
        # Estimate tokens and trim if needed
        estimated_tokens = 0
        for turn in reversed(list(self.turns)):
            turn_tokens = len(turn.content.split()) * 1.3  # Rough estimate
            if estimated_tokens + turn_tokens > self.max_tokens:
                break
            messages.insert(0, {
                "role": turn.role,
                "content": turn.content
            })
            estimated_tokens += turn_tokens
        
        return messages
    
    def set_context(self, key: str, value: any):
        """Set session context variable."""
        self.context[key] = value
    
    def get_context(self, key: str, default: any = None) -> any:
        """Get session context variable."""
        return self.context.get(key, default)
    
    def summarize(self) -> str:
        """Create a summary of the conversation for long-term storage."""
        if not self.turns:
            return ""
        
        # Use LLM to summarize
        conversation_text = "\n".join([
            f"{t.role}: {t.content}" for t in self.turns
        ])
        
        # This would call the LLM
        return f"Conversation with {len(self.turns)} turns"
```

### 7.3 User Profile Management

```python
from pydantic import BaseModel, Field
from typing import List, Optional
import json

class UserProfile(BaseModel):
    """Stores persistent user information."""
    
    user_id: str
    name: str
    preferred_name: Optional[str] = None
    title: str = "sir"  # How JARVIS addresses the user
    
    # Preferences
    temperature_unit: str = "fahrenheit"
    time_format: str = "12h"
    wake_word: str = "jarvis"
    voice_preference: str = "echo"  # TTS voice
    
    # Patterns learned
    typical_wake_time: Optional[str] = None
    typical_sleep_time: Optional[str] = None
    work_schedule: Optional[dict] = None
    
    # Interests and context
    interests: List[str] = Field(default_factory=list)
    home_location: Optional[dict] = None  # {lat, lon, city}
    work_location: Optional[dict] = None
    
    # Privacy settings
    store_conversations: bool = True
    allow_proactive: bool = True
    local_only_topics: List[str] = Field(default_factory=list)

class UserProfileManager:
    def __init__(self, storage_path: str = "./user_profiles"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.profiles: dict[str, UserProfile] = {}
        self._load_profiles()
    
    def _load_profiles(self):
        """Load all user profiles from storage."""
        for file in self.storage_path.glob("*.json"):
            with open(file, "r") as f:
                data = json.load(f)
                profile = UserProfile(**data)
                self.profiles[profile.user_id] = profile
    
    def save_profile(self, profile: UserProfile):
        """Save a user profile."""
        self.profiles[profile.user_id] = profile
        
        file_path = self.storage_path / f"{profile.user_id}.json"
        with open(file_path, "w") as f:
            json.dump(profile.model_dump(), f, indent=2)
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get a user profile."""
        return self.profiles.get(user_id)
    
    def create_default_profile(self, user_id: str, name: str) -> UserProfile:
        """Create a new user profile with defaults."""
        profile = UserProfile(
            user_id=user_id,
            name=name
        )
        self.save_profile(profile)
        return profile
```

---

## 8. Tool & API Integration

### 8.1 Web Search Integration

```python
from tavily import TavilyClient

class WebSearchTool:
    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key)
    
    async def search(self, query: str, max_results: int = 5) -> dict:
        """Perform a web search."""
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_answer=True,
            include_raw_content=False
        )
        
        return {
            "answer": response.get("answer", ""),
            "results": [
                {
                    "title": r["title"],
                    "url": r["url"],
                    "snippet": r["content"][:200]
                }
                for r in response.get("results", [])
            ]
        }

@tool("web_search")
async def web_search(query: str) -> str:
    """Search the web for current information."""
    
    searcher = WebSearchTool(api_key=os.getenv("TAVILY_API_KEY"))
    results = await searcher.search(query)
    
    if results["answer"]:
        return results["answer"]
    
    # Format results for voice
    formatted = []
    for r in results["results"][:3]:
        formatted.append(f"From {r['title']}: {r['snippet']}")
    
    return " ".join(formatted)
```

### 8.2 Calendar Integration (Google Calendar)

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

class CalendarIntegration:
    def __init__(self, credentials_path: str):
        creds = Credentials.from_authorized_user_file(credentials_path)
        self.service = build('calendar', 'v3', credentials=creds)
    
    async def get_events(
        self, 
        calendar_id: str = 'primary',
        days_ahead: int = 1
    ) -> list:
        """Get upcoming calendar events."""
        
        now = datetime.utcnow().isoformat() + 'Z'
        end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'
        
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            timeMax=end,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        return [
            {
                "title": event['summary'],
                "start": event['start'].get('dateTime', event['start'].get('date')),
                "end": event['end'].get('dateTime', event['end'].get('date')),
                "location": event.get('location', ''),
                "description": event.get('description', '')
            }
            for event in events
        ]
    
    async def create_event(
        self,
        title: str,
        start: datetime,
        end: datetime,
        description: str = "",
        location: str = "",
        calendar_id: str = 'primary'
    ) -> dict:
        """Create a new calendar event."""
        
        event = {
            'summary': title,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start.isoformat(),
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end.isoformat(),
                'timeZone': 'America/New_York',
            },
        }
        
        event = self.service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()
        
        return {"id": event['id'], "link": event.get('htmlLink')}

@tool("get_schedule")
async def get_schedule(timeframe: str = "today") -> str:
    """Get the user's calendar schedule."""
    
    calendar = CalendarIntegration(credentials_path="./credentials/google.json")
    
    days = {"today": 1, "tomorrow": 2, "this week": 7}.get(timeframe.lower(), 1)
    events = await calendar.get_events(days_ahead=days)
    
    if not events:
        return f"You have no events scheduled for {timeframe}."
    
    # Format for voice
    formatted = []
    for event in events:
        start = datetime.fromisoformat(event["start"].replace('Z', '+00:00'))
        time_str = start.strftime("%I:%M %p")
        formatted.append(f"At {time_str}: {event['title']}")
    
    return f"Your schedule for {timeframe}: " + ". ".join(formatted)

@tool("schedule_meeting")
async def schedule_meeting(
    title: str,
    date: str,
    time: str,
    duration_minutes: int = 60
) -> str:
    """Schedule a new meeting or event."""
    
    calendar = CalendarIntegration(credentials_path="./credentials/google.json")
    
    # Parse date and time
    from dateparser import parse
    start = parse(f"{date} {time}")
    end = start + timedelta(minutes=duration_minutes)
    
    result = await calendar.create_event(
        title=title,
        start=start,
        end=end
    )
    
    return f"I've scheduled '{title}' for {start.strftime('%B %d at %I:%M %p')}."
```

### 8.3 Weather Integration

```python
import httpx

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    async def get_current(self, lat: float, lon: float) -> dict:
        """Get current weather."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/weather",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "imperial"
                }
            )
            data = response.json()
            
            return {
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
    
    async def get_forecast(self, lat: float, lon: float, days: int = 3) -> list:
        """Get weather forecast."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/forecast",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "imperial",
                    "cnt": days * 8  # 3-hour intervals
                }
            )
            data = response.json()
            
            # Group by day
            forecasts = []
            current_date = None
            
            for item in data["list"]:
                date = item["dt_txt"].split()[0]
                if date != current_date:
                    current_date = date
                    forecasts.append({
                        "date": date,
                        "high": item["main"]["temp_max"],
                        "low": item["main"]["temp_min"],
                        "description": item["weather"][0]["description"]
                    })
            
            return forecasts[:days]

@tool("get_weather")
async def get_weather(location: str = "current", forecast: bool = False) -> str:
    """Get weather information."""
    
    weather = WeatherService(api_key=os.getenv("OPENWEATHER_API_KEY"))
    
    # Get coordinates (use user's home location or geocode)
    if location == "current":
        lat, lon = 40.7128, -74.0060  # Default NYC, should use user profile
    else:
        # Geocode the location
        lat, lon = await geocode_location(location)
    
    if forecast:
        forecasts = await weather.get_forecast(lat, lon)
        parts = []
        for f in forecasts:
            parts.append(f"{f['date']}: {f['description']}, high of {f['high']:.0f}°")
        return "Here's the forecast: " + ". ".join(parts)
    else:
        current = await weather.get_current(lat, lon)
        return (
            f"Currently it's {current['temperature']:.0f}° and {current['description']}. "
            f"Feels like {current['feels_like']:.0f}° with {current['humidity']}% humidity."
        )
```

### 8.4 Email Integration (Gmail)

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

class EmailIntegration:
    def __init__(self, credentials_path: str):
        creds = Credentials.from_authorized_user_file(credentials_path)
        self.service = build('gmail', 'v1', credentials=creds)
    
    async def get_unread_emails(self, max_results: int = 5) -> list:
        """Get unread emails."""
        
        results = self.service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        emails = []
        for msg in messages:
            full_msg = self.service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['Subject', 'From', 'Date']
            ).execute()
            
            headers = {h['name']: h['value'] for h in full_msg['payload']['headers']}
            
            emails.append({
                "id": msg['id'],
                "subject": headers.get('Subject', '(No Subject)'),
                "from": headers.get('From', 'Unknown'),
                "date": headers.get('Date', ''),
                "snippet": full_msg.get('snippet', '')
            })
        
        return emails
    
    async def send_email(self, to: str, subject: str, body: str) -> dict:
        """Send an email."""
        
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        sent = self.service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        
        return {"id": sent['id'], "status": "sent"}

@tool("check_email")
async def check_email() -> str:
    """Check for new unread emails."""
    
    email_client = EmailIntegration(credentials_path="./credentials/google.json")
    emails = await email_client.get_unread_emails()
    
    if not emails:
        return "You have no unread emails."
    
    # Format for voice
    parts = [f"You have {len(emails)} unread email{'s' if len(emails) > 1 else ''}:"]
    
    for email in emails[:3]:  # Limit to 3 for voice
        sender = email['from'].split('<')[0].strip()
        parts.append(f"From {sender}: {email['subject']}")
    
    return " ".join(parts)
```

### 8.5 Tool Registry

```python
from typing import List, Callable, Dict, Any
from langchain.tools import BaseTool

class ToolRegistry:
    """Central registry for all JARVIS tools."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._categories: Dict[str, List[str]] = {}
    
    def register(
        self, 
        tool: BaseTool, 
        category: str = "general"
    ):
        """Register a tool."""
        self._tools[tool.name] = tool
        
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(tool.name)
    
    def get_tool(self, name: str) -> BaseTool:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def get_tools_by_category(self, category: str) -> List[BaseTool]:
        """Get all tools in a category."""
        tool_names = self._categories.get(category, [])
        return [self._tools[name] for name in tool_names]
    
    def get_all_tools(self) -> List[BaseTool]:
        """Get all registered tools."""
        return list(self._tools.values())
    
    def get_tool_descriptions(self) -> str:
        """Get formatted tool descriptions for prompts."""
        descriptions = []
        for name, tool in self._tools.items():
            descriptions.append(f"- {name}: {tool.description}")
        return "\n".join(descriptions)

# Initialize and register tools
tool_registry = ToolRegistry()

# Smart Home Tools
tool_registry.register(control_lights, category="smart_home")
tool_registry.register(set_thermostat, category="smart_home")
tool_registry.register(get_home_status, category="smart_home")

# Information Tools
tool_registry.register(web_search, category="information")
tool_registry.register(get_weather, category="information")

# Task Tools
tool_registry.register(get_schedule, category="tasks")
tool_registry.register(schedule_meeting, category="tasks")
tool_registry.register(check_email, category="tasks")

# Vision Tools
tool_registry.register(analyze_camera, category="vision")
tool_registry.register(who_is_at_door, category="vision")
```

---

## 9. User Interface Options

### 9.1 Web Dashboard (React)

```typescript
// src/App.tsx
import React, { useState, useEffect, useRef } from 'react';
import { Room, RoomEvent, Track } from 'livekit-client';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const JARVISDashboard: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isListening, setIsListening] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected'>('disconnected');
  
  const roomRef = useRef<Room | null>(null);

  useEffect(() => {
    connectToJARVIS();
    return () => {
      roomRef.current?.disconnect();
    };
  }, []);

  const connectToJARVIS = async () => {
    setConnectionStatus('connecting');
    
    // Get token from your backend
    const response = await fetch('/api/get-token');
    const { token, url } = await response.json();
    
    const room = new Room();
    roomRef.current = room;
    
    room.on(RoomEvent.TrackSubscribed, (track) => {
      if (track.kind === Track.Kind.Audio) {
        // Play JARVIS audio response
        const audioElement = track.attach();
        document.body.appendChild(audioElement);
      }
    });
    
    room.on(RoomEvent.DataReceived, (payload) => {
      const data = JSON.parse(new TextDecoder().decode(payload));
      if (data.type === 'transcript') {
        addMessage('user', data.text);
      } else if (data.type === 'response') {
        addMessage('assistant', data.text);
      }
    });
    
    await room.connect(url, token);
    setConnectionStatus('connected');
  };

  const addMessage = (role: 'user' | 'assistant', content: string) => {
    setMessages(prev => [...prev, { role, content, timestamp: new Date() }]);
  };

  const startListening = async () => {
    setIsListening(true);
    // LiveKit handles audio capture automatically
    await roomRef.current?.localParticipant.setMicrophoneEnabled(true);
  };

  const stopListening = async () => {
    setIsListening(false);
    await roomRef.current?.localParticipant.setMicrophoneEnabled(false);
  };

  return (
    <div className="jarvis-dashboard">
      <header>
        <h1>J.A.R.V.I.S.</h1>
        <div className={`status ${connectionStatus}`}>
          {connectionStatus}
        </div>
      </header>
      
      <main className="chat-container">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <span className="role">{msg.role === 'user' ? 'You' : 'JARVIS'}:</span>
            <span className="content">{msg.content}</span>
          </div>
        ))}
      </main>
      
      <footer>
        <button
          className={`listen-button ${isListening ? 'active' : ''}`}
          onMouseDown={startListening}
          onMouseUp={stopListening}
          onMouseLeave={stopListening}
        >
          {isListening ? '🎙️ Listening...' : '🎤 Hold to Speak'}
        </button>
      </footer>
    </div>
  );
};

export default JARVISDashboard;
```

### 9.2 Mobile App (React Native)

```typescript
// App.tsx
import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Room, RoomEvent, Track } from 'livekit-client';
import { Audio } from 'expo-av';

const JARVISMobile: React.FC = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [lastResponse, setLastResponse] = useState('');

  const connectAndListen = async () => {
    // Request microphone permissions
    const { status } = await Audio.requestPermissionsAsync();
    if (status !== 'granted') {
      alert('Microphone permission is required');
      return;
    }

    // Connect to LiveKit and start voice session
    // ... implementation similar to web
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>J.A.R.V.I.S.</Text>
      
      <View style={styles.responseContainer}>
        <Text style={styles.response}>{lastResponse || 'Ready to assist, sir.'}</Text>
      </View>
      
      <TouchableOpacity
        style={[styles.button, isListening && styles.buttonActive]}
        onPressIn={() => setIsListening(true)}
        onPressOut={() => setIsListening(false)}
      >
        <Text style={styles.buttonText}>
          {isListening ? '🎙️ Listening...' : '🎤 Hold to Speak'}
        </Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a0a',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 32,
    color: '#00d4ff',
    marginBottom: 40,
  },
  responseContainer: {
    flex: 1,
    justifyContent: 'center',
  },
  response: {
    fontSize: 18,
    color: '#ffffff',
    textAlign: 'center',
  },
  button: {
    backgroundColor: '#1a1a2e',
    padding: 30,
    borderRadius: 100,
    borderWidth: 2,
    borderColor: '#00d4ff',
  },
  buttonActive: {
    backgroundColor: '#00d4ff',
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 18,
  },
});

export default JARVISMobile;
```

### 9.3 Desktop App (Electron)

```javascript
// main.js
const { app, BrowserWindow, globalShortcut, Tray, Menu } = require('electron');
const path = require('path');

let mainWindow;
let tray;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 400,
    height: 600,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  mainWindow.loadFile('index.html');
  
  // Hide on blur (optional)
  mainWindow.on('blur', () => {
    mainWindow.hide();
  });
}

function createTray() {
  tray = new Tray(path.join(__dirname, 'assets/icon.png'));
  
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Show JARVIS', click: () => mainWindow.show() },
    { label: 'Settings', click: () => openSettings() },
    { type: 'separator' },
    { label: 'Quit', click: () => app.quit() },
  ]);
  
  tray.setContextMenu(contextMenu);
  tray.on('click', () => mainWindow.show());
}

app.whenReady().then(() => {
  createWindow();
  createTray();
  
  // Global hotkey to activate JARVIS
  globalShortcut.register('CommandOrControl+Shift+J', () => {
    if (mainWindow.isVisible()) {
      mainWindow.hide();
    } else {
      mainWindow.show();
      mainWindow.webContents.send('activate-listening');
    }
  });
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});
```

### 9.4 Hardware Options for Dedicated Device

**Option A: Raspberry Pi 5 with Voice HAT**
- Hardware: Raspberry Pi 5 (8GB), ReSpeaker 4-Mic Array
- Cost: ~$150
- Ideal for: Fixed location, always-on assistant

**Option B: NVIDIA Jetson Orin Nano**
- Hardware: Jetson Orin Nano, USB microphone array
- Cost: ~$499
- Ideal for: Local AI processing, vision capabilities

**Option C: Custom Build with Mini PC**
- Hardware: Intel NUC/AMD Ryzen Mini PC + USB mic + speakers
- Cost: ~$400-800
- Ideal for: Maximum performance, expandability

---

## 10. Security & Privacy

### 10.1 Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    NETWORK LAYER                         │    │
│  │  • TLS 1.3 for all connections                          │    │
│  │  • VPN for remote access (Tailscale/WireGuard)          │    │
│  │  • Firewall rules (allow only necessary ports)          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                 APPLICATION LAYER                        │    │
│  │  • JWT authentication for API access                    │    │
│  │  • Role-based access control (RBAC)                     │    │
│  │  • Rate limiting on all endpoints                       │    │
│  │  • Input validation and sanitization                    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    DATA LAYER                            │    │
│  │  • Encryption at rest (AES-256)                         │    │
│  │  • Encryption in transit (TLS)                          │    │
│  │  • Secure key management (HashiCorp Vault)              │    │
│  │  • Regular backups with encryption                      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   PRIVACY LAYER                          │    │
│  │  • Local processing for sensitive data                  │    │
│  │  • Data minimization principles                         │    │
│  │  • User consent management                              │    │
│  │  • Audit logging                                        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 10.2 Authentication & Authorization

```python
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        return user_id

# Voice authentication (speaker verification)
class VoiceAuthService:
    def __init__(self):
        from speechbrain.pretrained import SpeakerRecognition
        self.verification = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb"
        )
    
    def verify_speaker(
        self, 
        audio_sample: bytes, 
        enrolled_sample_path: str,
        threshold: float = 0.25
    ) -> bool:
        """Verify if audio sample matches enrolled speaker."""
        
        # Save temporary file for processing
        temp_path = "/tmp/voice_sample.wav"
        with open(temp_path, "wb") as f:
            f.write(audio_sample)
        
        score, prediction = self.verification.verify_files(
            temp_path, 
            enrolled_sample_path
        )
        
        return score > threshold
```

### 10.3 Data Encryption

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class EncryptionService:
    def __init__(self, master_key: str):
        # Derive encryption key from master key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'jarvis_salt_v1',  # Should be stored securely
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        self.fernet = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data."""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data."""
        return self.fernet.decrypt(encrypted_data.encode()).decode()
    
    def encrypt_file(self, input_path: str, output_path: str):
        """Encrypt a file."""
        with open(input_path, 'rb') as f:
            data = f.read()
        
        encrypted = self.fernet.encrypt(data)
        
        with open(output_path, 'wb') as f:
            f.write(encrypted)
    
    def decrypt_file(self, input_path: str, output_path: str):
        """Decrypt a file."""
        with open(input_path, 'rb') as f:
            encrypted = f.read()
        
        decrypted = self.fernet.decrypt(encrypted)
        
        with open(output_path, 'wb') as f:
            f.write(decrypted)
```

### 10.4 Privacy Controls

```python
class PrivacyManager:
    """Manages data privacy and user consent."""
    
    def __init__(self, user_profile: UserProfile):
        self.profile = user_profile
        self.sensitive_categories = [
            "financial",
            "health",
            "personal_relationships",
            "passwords",
            "legal"
        ]
    
    def should_process_locally(self, request: str) -> bool:
        """Determine if request should be processed locally only."""
        
        # Check explicit local-only topics
        for topic in self.profile.local_only_topics:
            if topic.lower() in request.lower():
                return True
        
        # Check for sensitive categories
        for category in self.sensitive_categories:
            if self._detect_category(request, category):
                return True
        
        return False
    
    def _detect_category(self, text: str, category: str) -> bool:
        """Detect if text contains sensitive category content."""
        category_keywords = {
            "financial": ["bank", "account", "password", "credit card", "ssn", "tax"],
            "health": ["doctor", "medication", "diagnosis", "symptom", "prescription"],
            "personal_relationships": ["relationship", "divorce", "affair"],
            "passwords": ["password", "pin", "secret", "key"],
            "legal": ["lawyer", "court", "lawsuit", "legal"]
        }
        
        keywords = category_keywords.get(category, [])
        return any(kw in text.lower() for kw in keywords)
    
    def redact_for_logging(self, text: str) -> str:
        """Redact sensitive information before logging."""
        import re
        
        # Redact common patterns
        patterns = [
            (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REDACTED]'),  # SSN
            (r'\b\d{16}\b', '[CARD_REDACTED]'),  # Credit card
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]'),
            (r'password[:\s]+\S+', 'password: [REDACTED]'),
        ]
        
        redacted = text
        for pattern, replacement in patterns:
            redacted = re.sub(pattern, replacement, redacted, flags=re.IGNORECASE)
        
        return redacted
    
    def get_consent_status(self, feature: str) -> bool:
        """Check if user has consented to a feature."""
        consent_mapping = {
            "store_conversations": self.profile.store_conversations,
            "proactive_suggestions": self.profile.allow_proactive,
            "cloud_processing": not bool(self.profile.local_only_topics),
        }
        return consent_mapping.get(feature, False)
```

### 10.5 Audit Logging

```python
import logging
from datetime import datetime
import json

class AuditLogger:
    def __init__(self, log_path: str = "./logs/audit.log"):
        self.logger = logging.getLogger("jarvis_audit")
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_path)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
    
    def log_event(
        self,
        event_type: str,
        user_id: str,
        action: str,
        details: dict = None,
        success: bool = True
    ):
        """Log an audit event."""
        
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "action": action,
            "success": success,
            "details": details or {}
        }
        
        self.logger.info(json.dumps(event))
    
    def log_api_access(self, user_id: str, endpoint: str, method: str):
        self.log_event("api_access", user_id, f"{method} {endpoint}")
    
    def log_tool_use(self, user_id: str, tool_name: str, parameters: dict):
        self.log_event(
            "tool_use", 
            user_id, 
            tool_name,
            {"parameters": parameters}
        )
    
    def log_authentication(self, user_id: str, method: str, success: bool):
        self.log_event(
            "authentication",
            user_id,
            method,
            success=success
        )
```

---

## 11. Infrastructure & Deployment

### 11.1 Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Main JARVIS Backend
  jarvis-core:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: jarvis-core
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEEPGRAM_API_KEY=${DEEPGRAM_API_KEY}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - HA_TOKEN=${HA_TOKEN}
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://jarvis:${DB_PASSWORD}@postgres:5432/jarvis
    volumes:
      - ./data/memory:/app/data/memory
      - ./data/profiles:/app/data/profiles
      - ./credentials:/app/credentials:ro
    depends_on:
      - redis
      - postgres
      - ollama
    networks:
      - jarvis-network

  # LiveKit Server (Voice)
  livekit:
    image: livekit/livekit-server:latest
    container_name: livekit
    restart: unless-stopped
    ports:
      - "7880:7880"
      - "7881:7881"
      - "7882:7882/udp"
    environment:
      - LIVEKIT_KEYS=${LIVEKIT_API_KEY}:${LIVEKIT_API_SECRET}
    command: --dev --bind 0.0.0.0
    networks:
      - jarvis-network

  # Local LLM (Ollama)
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ./data/ollama:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    networks:
      - jarvis-network

  # Home Assistant
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:stable
    container_name: homeassistant
    restart: unless-stopped
    privileged: true
    ports:
      - "8123:8123"
    volumes:
      - ./data/homeassistant:/config
      - /etc/localtime:/etc/localtime:ro
    networks:
      - jarvis-network

  # Vector Database
  chromadb:
    image: chromadb/chroma:latest
    container_name: chromadb
    restart: unless-stopped
    ports:
      - "8001:8000"
    volumes:
      - ./data/chroma:/chroma/chroma
    environment:
      - ANONYMIZED_TELEMETRY=false
    networks:
      - jarvis-network

  # Redis (Cache & Message Queue)
  redis:
    image: redis:7-alpine
    container_name: redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - ./data/redis:/data
    command: redis-server --appendonly yes
    networks:
      - jarvis-network

  # PostgreSQL (Relational Data)
  postgres:
    image: postgres:15-alpine
    container_name: postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=jarvis
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=jarvis
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    networks:
      - jarvis-network

  # Web Dashboard
  jarvis-web:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: jarvis-web
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://jarvis-core:8000
      - NEXT_PUBLIC_LIVEKIT_URL=ws://livekit:7880
    networks:
      - jarvis-network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - jarvis-core
      - jarvis-web
    networks:
      - jarvis-network

networks:
  jarvis-network:
    driver: bridge
```

### 11.2 Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m jarvis && chown -R jarvis:jarvis /app
USER jarvis

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 11.3 Environment Configuration

```bash
# .env.example
# LLM APIs
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Voice APIs
DEEPGRAM_API_KEY=...
ELEVENLABS_API_KEY=...
PICOVOICE_ACCESS_KEY=...

# LiveKit
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
LIVEKIT_URL=ws://localhost:7880

# Home Assistant
HA_URL=http://homeassistant:8123
HA_TOKEN=...

# External Services
TAVILY_API_KEY=...
OPENWEATHER_API_KEY=...

# Database
DB_PASSWORD=secure_password_here
DATABASE_URL=postgresql://jarvis:${DB_PASSWORD}@postgres:5432/jarvis

# Security
JWT_SECRET_KEY=your_super_secret_jwt_key
ENCRYPTION_KEY=your_32_byte_encryption_key

# Logging
LOG_LEVEL=INFO
```

### 11.4 Kubernetes Deployment (Optional - for Scale)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jarvis-core
  labels:
    app: jarvis
spec:
  replicas: 2
  selector:
    matchLabels:
      app: jarvis
      component: core
  template:
    metadata:
      labels:
        app: jarvis
        component: core
    spec:
      containers:
      - name: jarvis-core
        image: your-registry/jarvis-core:latest
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: jarvis-secrets
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: jarvis-core
spec:
  selector:
    app: jarvis
    component: core
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

---

## 12. Development Phases

### Phase 1: Foundation (Weeks 1-4)
**Goal:** Basic voice interaction with smart home control

**Deliverables:**
- [ ] Project setup (Docker, CI/CD, repo structure)
- [ ] Wake word detection working
- [ ] Basic STT → LLM → TTS pipeline
- [ ] Home Assistant integration (lights, thermostat)
- [ ] Simple web dashboard

**Acceptance Criteria:**
- Can say "Hey JARVIS, turn on the lights" and lights turn on
- Response latency under 2 seconds
- 95% wake word detection accuracy

### Phase 2: Intelligence (Weeks 5-8)
**Goal:** Multi-agent orchestration with memory

**Deliverables:**
- [ ] LangGraph agent architecture
- [ ] Memory system (ChromaDB)
- [ ] Web search integration
- [ ] Calendar and email integration
- [ ] User profile management

**Acceptance Criteria:**
- JARVIS remembers previous conversations
- Can answer questions with web search
- Can read calendar and create events
- Correctly routes to specialized agents

### Phase 3: Polish (Weeks 9-12)
**Goal:** Production-ready voice experience

**Deliverables:**
- [ ] OpenAI Realtime API integration
- [ ] Interruption handling
- [ ] Improved TTS with emotion
- [ ] Mobile app (React Native)
- [ ] Error handling and recovery

**Acceptance Criteria:**
- Voice-to-voice latency under 800ms
- Natural conversation flow with interruptions
- Works reliably on mobile

### Phase 4: Advanced Features (Weeks 13-16)
**Goal:** Computer vision and proactive features

**Deliverables:**
- [ ] Camera integration
- [ ] Face recognition
- [ ] Object detection
- [ ] Proactive notifications
- [ ] Routine automation

**Acceptance Criteria:**
- Can identify who is at the door
- Proactively provides relevant information
- Automated morning/evening routines

### Phase 5: Security & Scale (Weeks 17-20)
**Goal:** Production security and scalability

**Deliverables:**
- [ ] Voice authentication
- [ ] End-to-end encryption
- [ ] Audit logging
- [ ] Performance optimization
- [ ] Documentation

**Acceptance Criteria:**
- All data encrypted at rest and in transit
- Passes security audit
- Handles multiple concurrent users

### Phase 6: Polish & Launch (Weeks 21-24)
**Goal:** Final polish and deployment

**Deliverables:**
- [ ] Beta testing with real users
- [ ] Bug fixes and improvements
- [ ] Deployment documentation
- [ ] Monitoring and alerting
- [ ] User onboarding flow

**Acceptance Criteria:**
- 99.5% uptime
- User satisfaction > 4.5/5
- Complete documentation

---

## 13. Testing Strategy

### 13.1 Unit Tests

```python
# tests/test_smart_home.py
import pytest
from unittest.mock import AsyncMock, patch
from jarvis.tools.smart_home import control_lights

@pytest.mark.asyncio
async def test_control_lights_turn_on():
    with patch('jarvis.tools.smart_home.HomeAssistantClient') as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.turn_on_light = AsyncMock(return_value={"success": True})
        
        result = await control_lights(
            room="living room",
            action="on",
            brightness=100
        )
        
        assert "Turned on lights in living room" in result
        mock_instance.turn_on_light.assert_called_once()

@pytest.mark.asyncio
async def test_control_lights_unknown_room():
    result = await control_lights(
        room="unknown_room",
        action="on"
    )
    
    assert "Unknown room" in result
```

### 13.2 Integration Tests

```python
# tests/integration/test_voice_pipeline.py
import pytest
from jarvis.voice import VoicePipeline

@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_voice_interaction():
    pipeline = VoicePipeline()
    
    # Simulate audio input
    audio_file = "tests/fixtures/turn_on_lights.wav"
    
    # Process through full pipeline
    transcript = await pipeline.transcribe(audio_file)
    assert "turn on" in transcript.lower() and "lights" in transcript.lower()
    
    response = await pipeline.process(transcript)
    assert "lights" in response.lower()
    
    audio_response = await pipeline.synthesize(response)
    assert len(audio_response) > 0
```

### 13.3 End-to-End Tests

```python
# tests/e2e/test_scenarios.py
import pytest
from playwright.async_api import async_playwright

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_web_dashboard_interaction():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto("http://localhost:3000")
        
        # Wait for connection
        await page.wait_for_selector(".status.connected")
        
        # Simulate voice input (using text for E2E)
        await page.fill("input.text-input", "What's the weather today?")
        await page.click("button.send")
        
        # Wait for response
        response = await page.wait_for_selector(".message.assistant")
        text = await response.inner_text()
        
        assert "weather" in text.lower() or "temperature" in text.lower()
        
        await browser.close()
```

### 13.4 Performance Tests

```python
# tests/performance/test_latency.py
import pytest
import time
import statistics

@pytest.mark.performance
@pytest.mark.asyncio
async def test_voice_latency():
    pipeline = VoicePipeline()
    
    latencies = []
    
    for _ in range(10):
        start = time.time()
        
        # Full voice interaction
        transcript = await pipeline.transcribe("tests/fixtures/hello.wav")
        response = await pipeline.process(transcript)
        await pipeline.synthesize(response)
        
        latency = time.time() - start
        latencies.append(latency)
    
    avg_latency = statistics.mean(latencies)
    p95_latency = statistics.quantiles(latencies, n=20)[18]
    
    assert avg_latency < 1.0, f"Average latency {avg_latency}s exceeds 1s"
    assert p95_latency < 1.5, f"P95 latency {p95_latency}s exceeds 1.5s"
```

---

## 14. Maintenance & Updates

### 14.1 Monitoring Setup

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'jarvis'
    static_configs:
      - targets: ['jarvis-core:8000']
    metrics_path: /metrics

  - job_name: 'livekit'
    static_configs:
      - targets: ['livekit:7881']
```

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
request_count = Counter(
    'jarvis_requests_total',
    'Total requests',
    ['endpoint', 'method', 'status']
)

request_latency = Histogram(
    'jarvis_request_latency_seconds',
    'Request latency',
    ['endpoint'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Voice metrics
voice_latency = Histogram(
    'jarvis_voice_latency_seconds',
    'Voice pipeline latency',
    ['stage'],  # stt, llm, tts
    buckets=[0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0]
)

# Tool usage
tool_usage = Counter(
    'jarvis_tool_usage_total',
    'Tool invocations',
    ['tool_name', 'success']
)

# Active sessions
active_sessions = Gauge(
    'jarvis_active_sessions',
    'Currently active voice sessions'
)
```

### 14.2 Backup Strategy

```bash
#!/bin/bash
# backup.sh - Run daily via cron

BACKUP_DIR="/backups/jarvis/$(date +%Y-%m-%d)"
mkdir -p $BACKUP_DIR

# PostgreSQL
docker exec postgres pg_dump -U jarvis jarvis | gzip > $BACKUP_DIR/postgres.sql.gz

# ChromaDB
tar -czf $BACKUP_DIR/chroma.tar.gz ./data/chroma

# User profiles and memory
tar -czf $BACKUP_DIR/profiles.tar.gz ./data/profiles ./data/memory

# Encrypt backups
gpg --encrypt --recipient backup@jarvis.local $BACKUP_DIR/*.gz
rm $BACKUP_DIR/*.gz $BACKUP_DIR/*.tar

# Sync to offsite storage
rclone sync $BACKUP_DIR remote:jarvis-backups/$(date +%Y-%m-%d)

# Cleanup old backups (keep 30 days)
find /backups/jarvis -type d -mtime +30 -exec rm -rf {} +
```

### 14.3 Update Procedure

```bash
#!/bin/bash
# update.sh - JARVIS update procedure

set -e

echo "=== JARVIS Update Procedure ==="

# 1. Create backup
echo "Creating backup..."
./backup.sh

# 2. Pull latest changes
echo "Pulling latest code..."
git pull origin main

# 3. Build new images
echo "Building new images..."
docker-compose build

# 4. Run database migrations
echo "Running migrations..."
docker-compose run --rm jarvis-core alembic upgrade head

# 5. Rolling restart
echo "Performing rolling restart..."
docker-compose up -d --no-deps jarvis-core
sleep 10  # Wait for health check

# 6. Verify health
echo "Verifying health..."
curl -f http://localhost:8000/health || {
    echo "Health check failed! Rolling back..."
    docker-compose down
    git checkout HEAD~1
    docker-compose up -d
    exit 1
}

echo "Update complete!"
```

---

## 15. Budget & Resource Estimates

### 15.1 Development Costs

| Role | Hours | Rate | Total |
|------|-------|------|-------|
| Backend Developer (Senior) | 400 | $100/hr | $40,000 |
| Frontend Developer | 200 | $80/hr | $16,000 |
| DevOps/Infrastructure | 100 | $100/hr | $10,000 |
| AI/ML Engineer | 150 | $120/hr | $18,000 |
| QA Engineer | 80 | $60/hr | $4,800 |
| **Total Development** | **930** | - | **$88,800** |

*Note: Costs vary significantly based on location and experience level. Freelance rates may range from 50-150% of these estimates.*

### 15.2 Infrastructure Costs (Monthly)

| Service | Provider | Cost |
|---------|----------|------|
| Cloud Server (4 vCPU, 16GB RAM) | DigitalOcean/Hetzner | $50-100 |
| LLM API (Claude/GPT) | Anthropic/OpenAI | $50-200 |
| Voice API (STT) | Deepgram | $30-100 |
| Voice API (TTS) | Inworld/ElevenLabs | $20-50 |
| LiveKit Cloud (optional) | LiveKit | $0-100 |
| Domain + SSL | Cloudflare | $0-20 |
| Monitoring | Self-hosted | $0 |
| **Total Monthly** | | **$150-570** |

### 15.3 Hardware (One-Time)

| Item | Purpose | Cost |
|------|---------|------|
| Development Machine | Local development | $0 (existing) |
| Raspberry Pi 5 + Accessories | Voice endpoint | $150 |
| Quality Microphone Array | Voice capture | $50-200 |
| Smart Speakers | Audio output | $50-200 |
| NVIDIA GPU (RTX 4070+) | Local LLM inference | $500-800 |
| **Total Hardware** | | **$750-1,350** |

### 15.4 External Services (Annual)

| Service | Purpose | Cost/Year |
|---------|---------|-----------|
| Picovoice | Wake word detection | $0-500 |
| Tavily | Web search | $0-500 |
| Weather API | Weather data | $0-100 |
| Domain registration | DNS | $15 |
| **Total Annual** | | **$15-1,115** |

---

## 16. Technical Appendices

### Appendix A: API Documentation Standards

```yaml
# OpenAPI specification for JARVIS API
openapi: 3.0.0
info:
  title: JARVIS API
  version: 1.0.0
  description: Personal AI Assistant API

paths:
  /api/v1/voice/session:
    post:
      summary: Create voice session
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: string
      responses:
        200:
          description: Session created
          content:
            application/json:
              schema:
                type: object
                properties:
                  session_id:
                    type: string
                  livekit_token:
                    type: string
                  livekit_url:
                    type: string

  /api/v1/chat:
    post:
      summary: Send text message
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                session_id:
                  type: string
      responses:
        200:
          description: Response generated
          content:
            application/json:
              schema:
                type: object
                properties:
                  response:
                    type: string
                  tools_used:
                    type: array
                    items:
                      type: string
```

### Appendix B: Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User preferences
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    key VARCHAR(255) NOT NULL,
    value JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, key)
);

-- Conversation history
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    session_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tool usage tracking
CREATE TABLE tool_invocations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    tool_name VARCHAR(255) NOT NULL,
    parameters JSONB,
    result JSONB,
    success BOOLEAN NOT NULL,
    latency_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    event_type VARCHAR(100) NOT NULL,
    action VARCHAR(255) NOT NULL,
    details JSONB,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at);
CREATE INDEX idx_tool_invocations_user ON tool_invocations(user_id);
CREATE INDEX idx_audit_log_user ON audit_log(user_id);
CREATE INDEX idx_audit_log_created ON audit_log(created_at);
```

### Appendix C: Recommended Reading & Resources

**Documentation:**
- LangGraph: https://langchain-ai.github.io/langgraph/
- LiveKit Agents: https://docs.livekit.io/agents/
- Home Assistant API: https://developers.home-assistant.io/
- Deepgram: https://developers.deepgram.com/
- Ultralytics YOLO: https://docs.ultralytics.com/

**Tutorials:**
- LiveKit Voice AI Quickstart: https://docs.livekit.io/agents/quickstart/
- LangChain Multi-Agent: https://docs.langchain.com/oss/python/langchain/multi-agent
- Ollama Getting Started: https://ollama.com/

**Communities:**
- LiveKit Slack: https://livekit.io/community
- LangChain Discord: https://discord.gg/langchain
- Home Assistant Community: https://community.home-assistant.io/

---

## Document Information

**Version:** 1.0.0
**Last Updated:** January 30, 2026
**Author:** Prepared for Mo by Claude

**Revision History:**
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-30 | Initial comprehensive specification |

---

*This document is intended to be a living specification. As development progresses, updates should be made to reflect architectural decisions, lessons learned, and technology changes.*
