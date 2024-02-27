import deepsearch as ds
from deepsearch.cps.client.components.data_indices import (
    ElasticProjectDataCollectionSource,
)
from deepsearch.cps.client.components.elastic import ElasticProjectDataCollectionSource
from deepsearch.cps.queries import CorpusSemanticQuery
from deepsearch.cps.queries.results import RAGResult, SearchResult, SearchResultItem
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

from ds_watsonx_assistant.dependencies import get_deepsearch_api

app = FastAPI()


class QueryResponseResultItem(BaseModel):
    doc_hash: str
    path_in_doc: str
    passage: str
    source_is_text: bool


class QueryResponse(BaseModel):
    results: list[QueryResponseResultItem]


@app.get("/")
async def read_root() -> dict:
    """
    Root hello world endpoint
    """
    return {"Hello": "World"}


@app.get(
    "/query/documents/private/{proj_key}/{index_key}",
    description="Run the semantic query on a private collection.",
)
async def query_private_documents(
    proj_key: str,
    index_key: str,
    query: str,
    num_items: int = 10,
    api: ds.CpsApi = Depends(get_deepsearch_api),
) -> QueryResponse:
    """
    Run the semantic query on a private collection
    """

    question_query = CorpusSemanticQuery(
        question=query,
        project=proj_key,
        index_key=index_key,
        # optional params:
        retr_k=num_items,
        # text_weight=TEXT_WEIGHT,
        # rerank=RERANK,
    )
    api_output = api.queries.run(question_query)
    search_result = SearchResult.from_api_output(api_output)

    return QueryResponse(
        results=[
            QueryResponseResultItem.model_validate_json(item.json())
            for item in search_result.search_result_items
        ]
    )