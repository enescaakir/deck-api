clients = set()

async def broadcast(message):
    disconnected = set()
    for client in clients:
        try:
            await client.send(message)
        except:
            disconnected.add(client)
    clients.difference_update(disconnected)
