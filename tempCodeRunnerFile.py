print("Sending order...")
    order = client.create_order(symbol=symbol,
                                side = side,
                                type = order_type,
                                quantity = quantity)
    print(order)
    return True