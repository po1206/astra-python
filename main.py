import os
from astrapy import DataAPIClient
from astrapy.constants import VectorMetric
from astrapy.ids import UUID
from astrapy.exceptions import InsertManyException

# Initialize the client and get a "Database" object
token = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
print(f"${token}")
client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])
print(f"* Database: {database.info().name}\n")

# Create a collection. The default similarity metric is consine. If you're not
# sure what dimension to set, user whatever dimension vector your embeddings
# model produces.

collection = database.create_collection(
    "vector_test",
    dimension=5,
    metric=VectorMetric.COSINE, # or simply "consine"
    check_exists=False,
)
print(f"* Collection: {collection.full_name}\n")

# Insert documents into the collection.
# (UUIDs here are version 7.)
documents = [
    {
        "_id": UUID("018e65c9-df45-7913-89f8-175f28bd7f74"),
        "text": "Chat bot integrated sneakers that talk to you",
        "$vector": [0.1, 0.15, 0.3, 0.12, 0.05],
    },
    {
        "_id": UUID("018e65c9-e1b7-7048-a593-db452be1e4c2"),
        "text": "An AI quilt to help you sleep forever",
        "$vector": [0.45, 0.09, 0.01, 0.2, 0.11],
    },
    {
        "_id": UUID("018e65c9-e33d-749b-9386-e848739582f0"),
        "text": "A deep learning display that controls your mood",
        "$vector": [0.1, 0.05, 0.08, 0.3, 0.6],
    },
]

try:
    insertion_result = collection.insert_many(documents)
    print(f"* Inserted {len(insertion_result.inserted_ids)} items.\n")
except InsertManyException:
    print("* Documents found on DB already. Let's move on.\n")

# Perform a similarity search
query_vector = [0.15, 0.1, 0.1, 0.35, 0.55]

results = collection.find(
    sort ={"$vector": query_vector},
    limit=10,
)

print("Vector search results:")
for document in results:
    print("    ", document)

# Cleanup (if desired)
drop_result = collection.drop()
print(f"\nCleanup: {drop_result}\n")
asdf

