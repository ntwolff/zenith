# ------------------------------
# @TODO - Persistance Layer
# ------------------------------
        
# app/stream/agents/events.py
    # from app.config import settings
    # from app.database.manager import DatabaseManager
    # from app.repositories.graph import GraphRepository
    # from app.repositories.cache import CacheRepository
    # from app.repositories.document import DocumentRepository
    #
    # db_manager = DatabaseManager(settings)
    # graph_repo = GraphRepository(db_manager)
    # cache_repo = CacheRepository(db_manager)
    # document_repo = DocumentRepository(db_manager)
    #
    # @faust_app.agent(event_topic)
    # async def event_ingestion(events):
    #     async for event in events:
    #         # Create event in Neo4j
    #         graph_repo.create_event(event)
    #   
    #         # Create event in MongoDB
    #         document_repo.create_event(event)
    #
    #         # Cache event in Redis
    #         cache_repo.set_event(event.id, event)


# app/jobs/sync.py
    # from app.config import settings
    # from app.database.manager import DatabaseManager
    # from app.repositories.graph import GraphRepository
    # from app.repositories.document import DocumentRepository
    #
    # db_manager = DatabaseManager(settings)
    # graph_repo = GraphRepository(db_manager)
    # document_repo = DocumentRepository(db_manager)
    #
    # def sync_events():
    #     # Retrieve events from Neo4j
    #     neo4j_events = graph_repo.get_events()
    #      
    #     # Retrieve events from MongoDB
    #     mongodb_events = document_repo.get_events()
    #       
    #     # Compare and synchronize events
    #     ...


# app/stream/agents/events.py
    # @faust_app.agent(event_topic)
    # async def event_ingestion(events):
    #     async for event in events:
    #         # Check if event exists in cache
    #         cached_event = cache_repo.get_event(event.id)
    #         if cached_event:
    #             # Event found in cache, skip database operations
    #             continue
    #           
    #         # Create event in databases
    #         ...
    #            
    #         # Cache event in Redis
    #         cache_repo.set_event(event.id, event)