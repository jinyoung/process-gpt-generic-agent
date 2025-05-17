import os
import openai
from datetime import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import chromadb
from chromadb.config import Settings

class KnowledgeToolSchema(BaseModel):
    agent_name: str = Field(..., description="에이전트 이름 (knowledge/{agent_name}/)")
    mode: str = Field(..., description="'add' 또는 'retrieve' 중 하나. add는 지식 축적, retrieve는 인출.")
    content: Optional[str] = Field(None, description="추가할 지식 내용 (mode=add일 때)")
    feedback: Optional[str] = Field(None, description="피드백 내용 (mode=add일 때 선택)")
    query: Optional[str] = Field(None, description="검색 쿼리 (mode=retrieve일 때)")

class KnowledgeTool(BaseTool):
    name: str = "knowledge_management"
    description: str = "에이전트별 마크다운 지식 관리 및 ChromaDB 기반 유사도 검색 툴. mode(add/retrieve)에 따라 지식 축적 또는 인출을 수행."
    args_schema: type = KnowledgeToolSchema

    def __init__(self):
        super().__init__()
        # 지식 관리 디렉토리가 없으면 생성
        self._ensure_knowledge_dir()
        
    def _ensure_knowledge_dir(self):
        """지식 관리 디렉토리 구조 확인 및 생성"""
        knowledge_dir = Path("knowledge")
        knowledge_dir.mkdir(exist_ok=True)
        
    def _get_collection(self, agent_name):
        # 에이전트별 지식 저장소 경로 생성
        agent_dir = Path(f"knowledge/{agent_name}")
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        chroma_dir = agent_dir / "chroma_db"
        chroma_dir.mkdir(exist_ok=True)
        
        client = chromadb.Client(Settings(
            persist_directory=str(chroma_dir)
        ))
        return client.get_or_create_collection(name="knowledge")

    def _embed(self, text):
        resp = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        return resp["data"][0]["embedding"]

    def _run(self, agent_name: str, mode: str, content: Optional[str] = None, feedback: Optional[str] = None, query: Optional[str] = None):
        collection = self._get_collection(agent_name)
        if mode == "add":
            if not content:
                return "content가 필요합니다."
            emb = self._embed(content)
            doc_id = f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
            metadata = {"content": content}
            if feedback:
                metadata["feedback"] = feedback
            collection.add(
                ids=[doc_id],
                embeddings=[emb],
                metadatas=[metadata],
                documents=[content]
            )
            # 마크다운 파일도 저장 (옵션)
            agent_dir = Path(f"knowledge/{agent_name}")
            agent_dir.mkdir(parents=True, exist_ok=True)
            file_path = agent_dir / f"{doc_id}.md"
            with open(file_path, "w") as f:
                f.write(f"# 발견 내용\n{content}\n")
                if feedback:
                    f.write(f"\n## 피드백\n{feedback}\n")
            return f"새 문서가 생성되었습니다: {file_path}"
        elif mode == "retrieve":
            if not query:
                return "query가 필요합니다."
            emb = self._embed(query)
            results = collection.query(
                query_embeddings=[emb],
                n_results=3
            )
            if not results["ids"][0]:
                return "지식이 없습니다."
            output = []
            for doc_id, metadata in zip(results["ids"][0], results["metadatas"][0]):
                agent_dir = Path(f"knowledge/{agent_name}")
                file_path = agent_dir / f"{doc_id}.md"
                if file_path.exists():
                    with open(file_path) as f:
                        output.append(f"[문서: {file_path}]\n" + f.read())
                else:
                    output.append(f"[ID: {doc_id}]\n{metadata.get('content', '')}")
            return "\n\n---\n\n".join(output)
        else:
            return "mode는 add 또는 retrieve만 지원합니다." 