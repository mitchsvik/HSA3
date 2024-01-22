import os
from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, Body, status
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from elasticsearch7 import Elasticsearch
from elasticsearch7.exceptions import NotFoundError
from motor.motor_asyncio import AsyncIOMotorClient


app = FastAPI()
es = Elasticsearch(hosts=[{'host': 'hsa3_elastic', 'port': 9200, 'password': os.environ['ELASTIC_PASSWORD'], 'use_ssl': False}])
mongo = AsyncIOMotorClient(os.environ['MONGO_URI'])
mongo_db = mongo.hsa3
timestamps_collection = mongo_db.timestamps

PyObjectId = Annotated[str, BeforeValidator(str)]


class TimestampModel(BaseModel):
    """Container for a single test entity"""
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    stamp: datetime = Field(default=datetime.now())
    day: int = Field(default=datetime.now().day)
    month: int = Field(default=datetime.now().month)
    year: int = Field(default=datetime.now().year)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            'example': {
                'stamp': '2024-01-01T00:00:00.000Z',
                'day': 1,
                'month': 1,
                'year': 2024
            }
        }
    )


class ElasticSearchResponseModel(BaseModel):
    """Container for a response"""
    hits: dict = {
        'total': {
            'value': int,
            'relation': str
        },
        'max_score': float,
        'hits': list
    }


class ResponseModelOnList(BaseModel):
    """Container for a response"""
    mongo: List[TimestampModel]
    es: ElasticSearchResponseModel


class ResponseModelOnCreate(BaseModel):
    """Container for a response"""
    mongo: TimestampModel
    es: dict


@app.get(
    '/',
    response_description='Get all timestamps',
    response_model=ResponseModelOnList,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False)
async def get_timestamps():
    """Get all timestamps from the database"""
    try:
        es_result = es.search(index='hsa3', body={'query': {'match_all': {}}})
    except NotFoundError:
        es_result = {'hits': {'hits': []}}
    mongo_result = await mongo.hsa3.timestamps.find().to_list(length=100)

    return {
        'mongo': mongo_result,
        'es': es_result
    }


@app.post(
    '/', 
    response_description='Add new timestamp', 
    response_model=ResponseModelOnCreate, 
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False
    )
async def create_timestamp(stamp: TimestampModel = Body(...)):
    """Add a new timestamp to the database"""
    is_index_exists = es.indices.exists(index='hsa3')
    if not is_index_exists:
        es.indices.create(index='hsa3')

    new_stamp_mongo = await timestamps_collection.insert_one(stamp.model_dump(by_alias=True, exclude={'id',}))
    new_stamp_es = es.index(index='hsa3', body=stamp.model_dump(by_alias=True, exclude={'id',}))

    created_stamp_mongo = await timestamps_collection.find_one({'_id': new_stamp_mongo.inserted_id})
    created_stamp_es = es.get(index='hsa3', id=new_stamp_es['_id'])

    return {
        'mongo': created_stamp_mongo,
        'es': created_stamp_es,
    }
