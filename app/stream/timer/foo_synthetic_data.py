# from app.models.v2.foo import Foo
# from app.models.v2.bar import Bar
# from app.stream.topic.foo import foo_topic
# from app.stream.faust_app import app
# from faker import Faker
# import random

# # Initialize Faker
# fake = Faker()

# @app.timer(1.0)
# async def send_foo() -> None: 
#     foo = Foo(uid=str(fake.uuid4()), name=fake.first_name(), bar=Bar(uid=str(fake.uuid4()), age=random.randint(18, 99)))
#     await foo_topic.send(value=foo)
#     print(f'Sent foo: {foo}')