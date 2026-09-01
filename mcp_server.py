#!/usr/bin/env python3
"""
MAGMA FastMCP server — stdio transport for VS Code, Cursor, and Claude Desktop.

VS Code launches this process; communication happens over stdin/stdout.
Do not print to stdout except through FastMCP protocol messages.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure project root is importable when launched from any cwd
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastmcp import FastMCP

from magma_service import get_service

mcp = FastMCP("magma")


def _json(data: dict) -> str:
    return json.dumps(data, indent=2, default=str)


@mcp.tool()
def magma_add(
    content: str,
    speaker: str | None = None,
    timestamp: str | None = None,
) -> str:
    """Store a fact or conversation turn in MAGMA long-term memory."""
    result = get_service().add(content=content, speaker=speaker, timestamp=timestamp)
    return _json(result)


@mcp.tool()
def magma_search(question: str, max_results: int = 10) -> str:
    """Retrieve relevant memory context for a question. Use the returned narrative_context to answer."""
    result = get_service().search(question=question, max_results=max_results)
    return _json(result)


@mcp.tool()
def magma_stats() -> str:
    """Return MAGMA memory statistics (node counts, vectors, links)."""
    return _json(get_service().stats())


@mcp.tool()
def magma_save() -> str:
    """Persist the current MAGMA graph and vectors to disk."""
    return _json(get_service().save())


if __name__ == "__main__":
    mcp.run(transport="stdio")
