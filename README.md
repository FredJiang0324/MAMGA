# MAGMA: A Multi-Graph based Agentic Memory Architecture

**A principled, multi-graph memory system for long-horizon agentic reasoning.**

<p align="center">
  <a href="https://arxiv.org/abs/2601.03236">
    <img src="https://img.shields.io/badge/Arxiv-paper-red" alt="MAGMA"
  </a>
</p>

<h5 align="center"> 🎉 If you are interested, please star ⭐ on GitHub for the latest update.</h5>

##  🔥 Research Highlights
- Read the full paper: <a href="https://arxiv.org/abs/2601.03236" target="_blank">https://arxiv.org/abs/2601.03236</a>


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
@article{jiang2026magma,
  title={MAGMA: A Multi-Graph based Agentic Memory Architecture for AI Agents},
  author={Jiang, Dongming and Li, Yi and Li, Guanpeng and Li, Bingzhe},
  journal={arXiv preprint arXiv:2601.03236},
  year={2026}
}
```


