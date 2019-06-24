from girder import events
from girder.plugin import GirderPlugin
from .utils import itemAddedToCollection, itemRemovedFromCollection
from .rest import (
    singleCollectionHandler,
    listCollectionHandler,
    forceRecomputeAllHandler,
    forceDeleteAllHandler,
    facetedSearchHandler
)


class GeoBrowserPlugin(GirderPlugin):
    DISPLAY_NAME = 'GeoBrowser Plugin'

    def load(self, info):
        events.bind('geometa.created', 'name',
                    itemAddedToCollection)
        # Add bind event for last item deleted in geometa collection
        # This is probably the wrong event
        # events.bind('model.item.remove', 'name',
        #             itemRemovedFromCollection)

        info['apiRoot'].collection.route(
            'GET',
            (':id', 'geobrowser'),
            singleCollectionHandler)

        info['apiRoot'].collection.route(
            'GET',
            ('geobrowser',),
            listCollectionHandler)

        info['apiRoot'].collection.route(
            'GET',
            ('geobrowser', 'search'),
            facetedSearchHandler)

        info['apiRoot'].collection.route(
            'PUT',
            ('geobrowser',),
            forceRecomputeAllHandler)

        info['apiRoot'].collection.route(
            'DELETE',
            ('geobrowser',),
            forceDeleteAllHandler)
