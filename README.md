# MAGMA: A Multi-Graph based Agentic Memory Architecture

**A principled, multi-graph memory system for long-horizon agentic reasoning.**

<p align="center">
  <a href="https://arxiv.org/abs/2601.03236">
    <img src="https://img.shields.io/badge/arXiv-2601.03236-b31b1b.svg" alt="arXiv">
  </a>
  <a href="https://huggingface.co/papers/2601.03236">
    <img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Paper-yellow" alt="Hugging Face">
  </a>
  <a href="https://github.com/FredJiang0324/MAMGA">
    <img src="https://img.shields.io/github/stars/FredJiang0324/MAMGA?style=social" alt="GitHub Stars">
  </a>
  <a href="https://aclanthology.org/2026.acl-long.1709/">
    <img src="https://img.shields.io/badge/ACL-2026%20Main-blue" alt="ACL 2026 Main">
  </a>
</p>

<h5 align="center"> 🎉 If you are interested, please star ⭐ on GitHub for the latest update.</h5>

## 📢 News

- **[2026/07]** MAGMA is now available on the **ACL Anthology**! Read it here: [![ACL Anthology](https://img.shields.io/badge/ACL-2026%20Main-blue)](https://aclanthology.org/2026.acl-long.1709/)
- **[2026/04/07]** MAGMA has been accepted by **ACL 2026** at the main conference! We will update the new version of the paper soon. Stay tuned!
- **[2026/01/06]** Our paper has been submitted to arXiv! Check it out: [![arXiv](https://img.shields.io/badge/arXiv-2601.03236-b31b1b.svg)](https://arxiv.org/abs/2601.03236)

##  🔥 Research Highlights
- Read the full paper: <a href="https://aclanthology.org/2026.acl-long.1709.pdf" target="_blank">https://aclanthology.org/2026.acl-long.1709.pdf</a>


## 📖 Overview

**MAGMA** (Multi-Graph based Agentic Memory Architecture) is a sophisticated memory system designed for long-term conversation memory and multi-hop reasoning. It creates interconnected event nodes linked by temporal, semantic, and causal relationships, enabling intelligent question answering across extended dialogues.



## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- Virtual environment (recommended)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/FredJiang0324/MAMGA.git
cd MAMGA
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Quick Start

### Testing with LoCoMo Dataset

```bash
# Test on LoCoMo dataset (10 samples included)
python test_fixed_memory.py --sample 0 --model gpt-4o-mini --max-questions 10 --category-to-test 1,2,3,4,5

# Test specific question categories
python test_fixed_memory.py --sample 0 --category-to-test 1  # Multi-hop only

# Test multiple samples
python test_fixed_memory.py --sample 0 1 2 --max-questions 50

# Full dataset path: data/locomo10.json
```

### Testing with LongMemEval Dataset

```bash
# Test with the main evaluation script (40% accuracy on multi-session)
python test_longmemeval_chunked.py --dataset data/longmemeval_s_cleaned.json --max-questions 5

# Test with sample data (included)
python test_longmemeval_chunked.py --dataset examples/longmemeval_sample.json --max-questions 5

# Note: Download longmemeval_s_cleaned.json separately (see Datasets section)
```

## Datasets

This system is evaluated on two primary datasets:

### 1. LoCoMo (Long Conversation Memory) - `data/locomo10.json`
- 10 conversation samples with extensive Q&A pairs
- 5 question categories: Multi-hop, Temporal, Open-domain, Single-hop, Adversarial
- Tests long-term memory and reasoning capabilities
- **Status**: Included in repository (2.7MB)

### 2. LongMemEval - `data/longmemeval_s_cleaned.json`
- Multi-session conversation dataset
- Focus on counting and aggregation across sessions
- Tests ability to track information across conversation boundaries
- **Status**: Download from HuggingFace (see instructions below)
- **Sample**: Small sample included in `examples/longmemeval_sample.json`

### Dataset Setup

1. **LoCoMo dataset** is included and ready to use

2. **LongMemEval dataset** - Download from HuggingFace:
```bash
mkdir -p data/
cd data/
wget https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned/resolve/main/longmemeval_s_cleaned.json
cd ..
```

## Configuration

### Embedding Models

- **MiniLM** (default): Fast, offline, 384-dimensional embeddings
- **OpenAI**: Higher quality, requires API key, 1536-dimensional embeddings

```bash
# Use MiniLM (default)
python test_fixed_memory.py --embedding-model minilm

# Use OpenAI embeddings
python test_fixed_memory.py --embedding-model openai
```

### LLM Models

Supports OpenAI models:
- `gpt-4o-mini` (Default)
- `gpt-4.1-mini` 
- `gpt-4o` 
- `gpt-3.5-turbo` 

### Cache Management

Memory is cached for efficiency:
```bash
# Default cache location
./locomo_trg_cache/sample{N}/

# Custom cache directory
python test_fixed_memory.py --cache-dir ./my_cache

# Force rebuild
python test_fixed_memory.py --rebuild
```

## Advanced Usage

### Query Engine Parameters

Configure retrieval behavior in `memory/query_engine.py`:

```python
# Retrieval parameters
vector_search_k = 20        # Initial vector search results
keyword_threshold = 0.3     # Minimum keyword score
top_k_final = 5            # Final context nodes
max_traversal_hops = 3     # Graph traversal depth
```

## MCP Integration (VS Code)

MAGMA runs as a **local FastMCP stdio server** — no separate hosted service required. VS Code launches `mcp_server.py` via [`.vscode/mcp.json`](.vscode/mcp.json).

> The same stdio server also works in **Cursor** (`.cursor/mcp.json` is included in this repo).

### Setup

1. Install dependencies (includes `fastmcp`):

```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` (optional but improves event extraction).

3. On macOS/Linux, change `venv/Scripts/python.exe` to `venv/bin/python` in `.vscode/mcp.json`.

4. In VS Code: **Command Palette** → **MCP: List Servers** → start **magma**.

5. Open **Copilot Agent** chat. Tools `magma_add`, `magma_search`, `magma_stats`, and `magma_save` should appear.

### MCP tools

| Tool | Purpose |
|------|---------|
| `magma_add` | Store a fact or conversation turn |
| `magma_search` | Retrieve graph context for a question |
| `magma_stats` | Node/vector/link counts |
| `magma_save` | Persist memory to disk |

Memory is stored under `MAGMA_PERSIST_DIR` (default `./magma_store`). `magma_add` auto-saves after each write.

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MAGMA_PERSIST_DIR` | `./magma_store` | Where graph and vectors are saved |
| `OPENAI_API_KEY` | — | Enables LLM-based event extraction (read from `.env`) |
| `DEFAULT_MODEL` | `gpt-4o-mini` | LLM model for extraction |
| `DEFAULT_EMBEDDING_MODEL` | `minilm` | `minilm` or `openai` |


## File Structure

```
trg-memory/
├── memory/                  # Core memory modules
│   ├── trg_memory.py       # Main memory engine
│   ├── graph_db.py         # Graph database
│   ├── vector_db.py        # Vector database
│   ├── query_engine.py     # Query processing
│   ├── memory_builder.py   # Memory construction
│   └── ...
├── magma_service.py        # Service layer for MCP
├── mcp_server.py           # FastMCP stdio server
├── .vscode/mcp.json        # MCP config (VS Code)
├── .cursor/mcp.json        # MCP config (Cursor, same server)
├── utils/                   # Utility modules
│   ├── memory_layer.py     # LLM controller
│   └── load_dataset.py     # Dataset loader
├── test_fixed_memory.py              # LoCoMo test script
├── test_longmemeval_chunked.py       # LongMemEval test script
├── load_longmemeval.py     # LongMemEval loader
├── examples/               # Sample datasets
├── data/                   # Full datasets (not included)
└── requirements.txt        # Dependencies
```

## Evaluation Metrics

The system uses multiple evaluation metrics:

- **Exact Match**: Binary correctness
- **F1 Score**: Token-level overlap (0-100%)
- **BLEU Score**: N-gram similarity (0-100%)
- **LLM Judge**: GPT-based semantic evaluation (0-100%)

## License

MIT License - see LICENSE file for details.

## Note

Have ideas or suggestions? Please feel free to submit issues or pull requests! 🚀

<span id='doc'/>

## 📖 Documentation

A more detailed documentation is coming soon 🚀, and we will update in the Github page.

<span id='cite'/>

## 📣 Citation
**If you find this project useful, please consider citing our paper:**

```bibtex
@inproceedings{jiang-etal-2026-magma,
    title = "{MAGMA}: A Multi-Graph based Agentic Memory Architecture for {AI} Agents",
    author = "Jiang, Dongming  and
      Li, Yi  and
      Li, Guanpeng  and
      Li, Bingzhe",
    editor = "Liakata, Maria  and
      Moreira, Viviane P.  and
      Zhang, Jiajun  and
      Jurgens, David",
    booktitle = "Proceedings of the 64th Annual Meeting of the {A}ssociation for {C}omputational {L}inguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2026",
    address = "San Diego, California, United States",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.acl-long.1709/",
    doi = "10.18653/v1/2026.acl-long.1709",
    pages = "36848--36865",
    ISBN = "979-8-89176-390-6",
    abstract = "Memory-Augmented Generation (MAG) extends large language models with external memory to support long-context reasoning, but existing approaches largely rely on semantic similarity over monolithic memory stores, entangling temporal, causal, and entity information. This design limits interpretability and alignment between query intent and retrieved evidence, leading to suboptimal reasoning accuracy. In this paper, we propose MAGMA, a multi-graph agentic memory architecture that represents each memory item across orthogonal semantic, temporal, causal, and entity graphs. MAGMA formulates retrieval as policy-guided traversal over these relational views, enabling query-adaptive selection and structured context construction. By decoupling memory representation from retrieval logic, MAGMA provides transparent reasoning paths and fine-grained control over retrieval. Experiments on LoCoMo and LongMemEval demonstrate that MAGMA consistently outperforms state-of-the-art agentic memory systems in long-horizon reasoning task."
}
```


