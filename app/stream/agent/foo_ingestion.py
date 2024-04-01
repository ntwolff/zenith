# from app.stream.faust_app import faust_app
# from app.stream.topic.foo import foo_topic

# @faust_app.agent(foo_topic)
# async def ingest_foo(foos):
#     async for foo in foos:
#         print(f'Ingested foo: {foo}')