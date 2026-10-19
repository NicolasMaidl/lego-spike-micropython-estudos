from hub import light_matrix, port, sound
import runloop, motor_pair, color_sensor, color, force_sensor, distance_sensor

def distancia():
    return distance_sensor.distance(port.C)

def velocidade():
    mm = distancia()
    if mm >= 200 or mm == -1:
        return 500
    elif mm < 200 and mm >= 100:
        return 250
    elif mm < 100 and mm >= 50:
        return 100
    else:
        return 0

def obstaculo():
    d = distancia()
    return (d != -1 and d < 50) or toque()

def toque():
    return force_sensor.pressed(port.D)

def vermelho():
    return color_sensor.color(port.E) == color.RED

async def musica():
    sound.volume(100)
    notas = [(523, 300), (659, 300), (784, 600),(659, 300), (523, 300), (440, 600),(392, 300), (440, 300), (523, 600)]
    for f,dur in notas:
        await sound.beep(f, dur)

async def coracao_pulsando():
    for _ in range(4):
        light_matrix.show_image(light_matrix.IMAGE_HEART)
        await runloop.sleep_ms(400)
        light_matrix.show_image(light_matrix.IMAGE_HEART_SMALL)
        await runloop.sleep_ms(400)

async def main():
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

    while True:
        if vermelho():
            motor_pair.stop(motor_pair.PAIR_1)
            await coracao_pulsando()
            await musica()
            break

        if obstaculo():
            motor_pair.stop(motor_pair.PAIR_1)
            while distancia() <= 50 or toque():
                await runloop.sleep_ms(50)
            await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1,360,600,-600)

        else:
            vel = velocidade()
            motor_pair.move(motor_pair.PAIR_1,0,velocity=vel)

        await runloop.sleep_ms(50)

runloop.run(main())
