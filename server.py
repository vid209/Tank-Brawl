import asyncio
import websockets

clients = {}
next_id = 1

async def handler(websocket):
    global next_id
    client_id = next_id
    next_id += 1
    clients[client_id] = websocket
    print(f"Игрок {client_id} подключился")
    
    # Отправляем игроку его ID (игра это ждёт)
    await websocket.send(f'{{"type":"id","id":{client_id}}}')
    
    try:
        async for message in websocket:
            # Пересылаем сообщение всем остальным игрокам
            for cid, ws in list(clients.items()):
                if cid != client_id:
                    try:
                        await ws.send(message)
                    except:
                        pass
    finally:
        if client_id in clients:
            del clients[client_id]
        print(f"Игрок {client_id} отключился")
        for ws in clients.values():
            try:
                await ws.send(f'{{"type":"disconnect","playerId":{client_id}}}')
            except:
                pass

async def main():
    # 0.0.0.0 — слушать на всех интерфейсах, включая Hamachi
    async with websockets.serve(handler, "0.0.0.0", 8080):
        print("Сервер запущен на порту 8080")
        print("Не закрывайте это окно, пока играете!")
        await asyncio.Future()

asyncio.run(main())