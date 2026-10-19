from hub import light_matrix, port, sound
import runloop, color, motor_pair, distance_sensor, color_sensor, force_sensor

noventagraus = 180
diametro_roda = 17.6

def cmporrot(cm):
    return int(cm / diametro_roda * 360)

def objetodetectado():
    distancia = distance_sensor.distance(port.D)
    return distancia > 0 and distancia < 100

def cor():
    return color_sensor.color(port.F) == color.BLACK

def toque():
    return force_sensor.pressed(port.C)

async def noventadireita():
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1,noventagraus,600,-600)

async def oito():
    distdeg = cmporrot(40)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1,distdeg,200,700)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1,distdeg,700,200)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1,distdeg,700,200)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1,distdeg,200,700)

async def caminhada():
    distdeg = cmporrot(30)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1,distdeg,360,360)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1,distdeg,-360,-360)

async def som_imagem():
    sound.volume(80)

    for _ in range(4):
        await sound.beep(440, 500)
        light_matrix.show_image(light_matrix.IMAGE_HAPPY)
        await runloop.sleep_ms(500)

        await sound.beep(550, 500)
        light_matrix.show_image(light_matrix.IMAGE_HEART)
        await runloop.sleep_ms(500)

        await sound.beep(660, 500)
        light_matrix.show_image(light_matrix.IMAGE_SAD)
        await runloop.sleep_ms(500)

        await sound.beep(770, 500)
        light_matrix.show_image(light_matrix.IMAGE_SURPRISED)
        await runloop.sleep_ms(500)

async def main():
    motor_pair.pair( motor_pair.PAIR_1, port.A, port.B)

    while True:
        motor_pair.move(motor_pair.PAIR_1, 0)
        await runloop.until(objetodetectado)
        motor_pair.stop(motor_pair.PAIR_1)
        await noventadireita()
        motor_pair.move(motor_pair.PAIR_1, 0)
        await runloop.until(cor)
        motor_pair.stop(motor_pair.PAIR_1)
        await oito()
        motor_pair.stop(motor_pair.PAIR_1)
        await runloop.until(toque)
        await caminhada()
        await som_imagem()

runloop.run(main())
