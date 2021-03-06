from datetime import datetime
from neo4j import GraphDatabase
from random import randint, choice
import psycopg2
import json
import sys

amounts = int(sys.argv[1])
orders = []

print(f'generating {amounts} orders')

####################################
####### DATABASE CONNECTIONS #######
####################################


def neo4j_query_get_items():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "1234"))
    with driver.session() as session:
        query = '''
            MATCH(item: Item) return item
        '''
        results = session.run(query)

    return results

####################################
##### DATABASE CONNECTIONS END #####
####################################


results = neo4j_query_get_items()
formatted_items = [{'id': record['item'].id, 'name': record['item']['name'], 'price': record['item']['price']} for record in results]


def random_item_list():
    types = randint(1, 10)
    items = []
    result = []

    while len(items) < types:
        item = choice(formatted_items)

        if item not in items:
            items.append(item)

    for item in items:
        amount = randint(1, 5)
        result.append({
            'item_id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'amount': amount,
        })

    return result


# generating data
for n in range(amounts):
    items = random_item_list()

    order = {
        'date': int(datetime.now().timestamp()) - randint(0, 2629743),
        'user_id': randint(1, 10_000),
        'items': items,
        'discount': None,
    }

    orders.append(order)

# saving to .json
with open('mongo-db/data/orders.json', 'w') as fp:
    json.dump(orders, fp, ensure_ascii=False)
    print(f'successfully added {len(orders)} orders to mongo-db/data/orders.json')
