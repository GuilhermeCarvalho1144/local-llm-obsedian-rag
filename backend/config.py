from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml
from pathlib import Path
from typing import List


class PathCfg(BaseModel):
    vault_path: str
    pdf_dirs: List[str] = Field(default_factory=list)
    data_dir: str = "./data"
    sqlite_path: str = "./data/second_brain.db"
    faiss_index_path: str = "./data/index.faiss"


class ChunkingCfg(BaseModel):
    max_chars: int = 8000
    overlap_chars: int = 600
    md_by_headings: bool = True
    keep_latex_blocks: bool = True


class RetrievalCfg(BaseModel):
    bm25_top_k: int = 25
    vector_top_k: int = 25
    final_top_k: int = 8
    diversify_max_per_doc: int = 2


class LlmCfg(BaseModel):
    provider: str
    model_path: str
    ctx: int = 4096
    temperature: float = 0.3
    max_new_tokens: int = 512
    n_gpu_layers: int = -1


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_", env_nested_delimiter="__", extra="ignore"
    )
    paths: PathCfg
    chunking: ChunkingCfg = ChunkingCfg()
    retrieval: RetrievalCfg = RetrievalCfg()
    llm: LlmCfg


def load_yaml(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


def load_settings(path: str = "config.yaml") -> AppSettings:
    data = load_yaml(path)
    return AppSettings.model_validate(data)
