import asyncio
import websockets

async def connect_websocket():
    uri = "wss://45.33.88.161:1337/"
    try:
        async with websockets.connect(uri, ssl=False) as websocket:
            # Envía un mensaje al servidor WebSocket
            await websocket.send("Hola, servidor WebSocket")

            # Espera la respuesta del servidor
            response = await websocket.recv()
            print(f"Respuesta del servidor: {response}")
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"Error de estado de respuesta: {e}")
    except websockets.exceptions.WebSocketProtocolError as e:
        print(f"Error de protocolo WebSocket: {e}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Error de conexión cerrada: {e}")
    except websockets.exceptions.SSLError as e:
        print(f"Error SSL/TLS: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

asyncio.get_event_loop().run_until_complete(connect_websocket())

