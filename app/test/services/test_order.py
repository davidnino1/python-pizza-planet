import pytest

def test_create_order_service(create_order):
    current_order = create_order.json
    pytest.assume(create_order.status.startswith('200'))
    pytest.assume(current_order['_id'])
    pytest.assume(current_order['client_address'])
    pytest.assume(current_order['client_dni'])
    pytest.assume(current_order['client_name'])
    pytest.assume(current_order['client_phone'])
    pytest.assume(current_order['date'])
    pytest.assume(current_order['detail'])
    pytest.assume(current_order['total_price'])

def test_get_order_by_id_service(client, create_order, order_url):
    current_order = create_order.json
    response = client.get(f'{order_url}id/{current_order["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_order = response.json
    for param, value in current_order.items():
        pytest.assume(returned_order[param] == value)

def test_get_orders_service(client, create_orders, order_url):
    response = client.get(order_url)
    pytest.assume(response.status.startswith('200'))
    returned_orders = {order['_id']: order for order in response.json}
    for order in create_orders:
        pytest.assume(order['_id'] in returned_orders)
