
import os
import json
import pytest

from girder.models.collection import Collection
# from geobrowser_plugin.rest import facetedSearchHandler


DATA_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    'data'))

SAMPLE_COLLECTION_DIR = os.path.join(
    DATA_DIR,
    'sample_collection_metadata')

SAMPLE_QUERY_DIR = os.path.join(
    DATA_DIR,
    'sample_collection_searches')


@pytest.fixture
def collectionsWithMeta(db):
    collections = []
    for filename in os.listdir(SAMPLE_COLLECTION_DIR):
        with open(f'{SAMPLE_COLLECTION_DIR}/{filename}', 'r') as file:
            collectionName = filename.split('.')[0]
            collection = Collection().createCollection(collectionName)
            collections.append(Collection().setMetadata(
                collection=collection, metadata=json.load(file)))

    return collections


@pytest.fixture
def sampleQueries():
    queries = []
    for filename in os.listdir(SAMPLE_QUERY_DIR):
        with open(f'{SAMPLE_QUERY_DIR}/{filename}', 'r') as file:
            queries.append(json.load(file))

    return queries


def test_search(collectionsWithMeta, sampleQueries):
    assert len(collectionsWithMeta) == 5
    assert len(sampleQueries) == 5
