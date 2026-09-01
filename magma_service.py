"""
MAGMA service layer for MCP integration.

Wraps TemporalResonanceGraphMemory with persistence and stderr-only logging
so stdio MCP transport stays clean.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from dateutil import parser as date_parser
from dotenv import load_dotenv

from memory.trg_memory import TemporalResonanceGraphMemory

load_dotenv()

# stdio MCP must not write logs to stdout
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "WARNING").upper(), logging.WARNING),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("magma_service")

_service: Optional["MagmaService"] = None


class MagmaService:
    """Singleton-friendly wrapper around TRG memory for MCP tools."""

    def __init__(
        self,
        persist_dir: Optional[str] = None,
        model: Optional[str] = None,
        embedding_model: Optional[str] = None,
    ):
        self.persist_dir = Path(
            persist_dir or os.getenv("MAGMA_PERSIST_DIR", "./magma_store")
        )
        self.model = model or os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
        self.embedding_model = embedding_model or os.getenv(
            "DEFAULT_EMBEDDING_MODEL", "minilm"
        )

        self.persist_dir.mkdir(parents=True, exist_ok=True)

        self.trg = TemporalResonanceGraphMemory(
            llm_backend="openai" if os.getenv("OPENAI_API_KEY") else None,
            llm_model=self.model,
            persist_dir=str(self.persist_dir),
            embedding_model=self.embedding_model,
            enable_async=False,
        )

        graph_file = self.persist_dir / "graph.json"
        if graph_file.exists():
            try:
                self.trg.load(str(self.persist_dir))
                logger.info("Loaded MAGMA store from %s", self.persist_dir)
            except Exception as exc:
                logger.warning("Could not load existing store: %s", exc)

    def add(
        self,
        content: str,
        speaker: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        metadata: Dict[str, Any] = {}
        if speaker:
            metadata["speaker"] = speaker

        parsed_ts: Optional[datetime] = None
        if timestamp:
            try:
                parsed_ts = date_parser.parse(timestamp)
            except (ValueError, TypeError) as exc:
                raise ValueError(f"Invalid timestamp: {timestamp}") from exc

        event_id = self.trg.add_event(
            interaction_content=content,
            timestamp=parsed_ts,
            metadata=metadata or None,
        )
        self.save()
        return {"event_id": event_id, "status": "stored"}

    def search(self, question: str, max_results: int = 10) -> Dict[str, Any]:
        context = self.trg.query(query_text=question, max_results=max_results)
        nodes = []
        for node in context.anchor_nodes[:max_results]:
            nodes.append(
                {
                    "node_id": node.node_id,
                    "timestamp": node.timestamp.isoformat()
                    if node.timestamp
                    else None,
                    "content": node.content_narrative,
                    "entities": node.attributes.get("entities", []),
                    "keywords": node.attributes.get("keywords", []),
                }
            )
        return {
            "question": question,
            "narrative_context": context.narrative_context,
            "anchor_nodes": nodes,
            "metadata": context.metadata,
        }

    def stats(self) -> Dict[str, Any]:
        return {
            "persist_dir": str(self.persist_dir),
            "model": self.model,
            "embedding_model": self.embedding_model,
            **self.trg.get_statistics(),
        }

    def save(self) -> Dict[str, str]:
        self.trg.save(str(self.persist_dir))
        return {"status": "saved", "path": str(self.persist_dir)}


def get_service() -> MagmaService:
    global _service
    if _service is None:
        _service = MagmaService()
    return _service
