from hub import port, motion_sensor
import motor, motor_pair, color_sensor, distance_sensor, force_sensor, runloop

motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

PORTA_TORRE = port.E
PORTA_ULTRASSONICO = port.C
PORTA_COR = port.D
PORTA_TOQUE = port.F

LIMIAR_PAREDE_MM = 100
VELOCIDADE_GIRO = 250
VELOCIDADE_GIRO_FINO = 60
VELOCIDADE_AVANCO = 450
CM_PER_ROT = 17.6

def deg_for_cm(cm):
    return int(cm / CM_PER_ROT * 360)

async def realizar_varredura():
    motor.run_to_relative_position(PORTA_TORRE, 90, 400)
    await runloop.sleep_ms(400)
    dist_direita = distance_sensor.distance(PORTA_ULTRASSONICO)
    print("Direita:", dist_direita)

    motor.run_to_relative_position(PORTA_TORRE, 0, 400)
    await runloop.sleep_ms(400)
    dist_frente = distance_sensor.distance(PORTA_ULTRASSONICO)
    print("Frente:", dist_frente)

    motor.run_to_relative_position(PORTA_TORRE, -90, 400)
    await runloop.sleep_ms(400)
    dist_esquerda = distance_sensor.distance(PORTA_ULTRASSONICO)
    print("Esquerda:", dist_esquerda)

    if dist_direita is not None and dist_direita != -1:
        d_dir = dist_direita
    else:
        d_dir = 999

    if dist_frente is not None and dist_frente != -1:
        d_fre = dist_frente
    else:
        d_fre = 999

    if dist_esquerda is not None and dist_esquerda != -1:
        d_esq = dist_esquerda
    else:
        d_esq = 999

    return d_dir, d_fre, d_esq

async def virar_angulo(angulo_alvo):
    motion_sensor.reset_yaw(0)
    await runloop.sleep_ms(50)

    alvo_total = abs(angulo_alvo * 10)
    alvo_fase1 = alvo_total - 150

    if angulo_alvo > 0:
        motor_pair.move_tank(motor_pair.PAIR_1, VELOCIDADE_GIRO, -VELOCIDADE_GIRO)
    else:
        motor_pair.move_tank(motor_pair.PAIR_1, -VELOCIDADE_GIRO, VELOCIDADE_GIRO)

    while abs(motion_sensor.tilt_angles()[0]) < alvo_fase1:
        await runloop.sleep_ms(10)

    if angulo_alvo > 0:
        motor_pair.move_tank(motor_pair.PAIR_1, VELOCIDADE_GIRO_FINO, -VELOCIDADE_GIRO_FINO)
    else:
        motor_pair.move_tank(motor_pair.PAIR_1, -VELOCIDADE_GIRO_FINO, VELOCIDADE_GIRO_FINO)

    while abs(motion_sensor.tilt_angles()[0]) < alvo_total:
        await runloop.sleep_ms(10)

    motor_pair.stop(motor_pair.PAIR_1)
    await runloop.sleep_ms(100)

async def avancar_uma_celula():
    motor.run_to_relative_position(PORTA_TORRE, 0, 400)
    pos_inicial = motor.relative_position(port.A)
    graus_20cm = deg_for_cm(20)

    motor_pair.move_for_degrees(motor_pair.PAIR_1, graus_20cm, 0, velocity=VELOCIDADE_AVANCO)

    while True:
        pos_atual = motor.relative_position(port.A)
        andado = abs(pos_atual - pos_inicial)

        if andado >= graus_20cm:
            break

        dist_frente = distance_sensor.distance(PORTA_ULTRASSONICO)
        if dist_frente is not None and dist_frente != -1:
            if dist_frente < 45:
                print("Parede muito proxima detectada durante o avanco! Parando antecipadamente.")
                break

        await runloop.sleep_ms(10)

    motor_pair.stop(motor_pair.PAIR_1)
    await runloop.sleep_ms(100)

async def detectou_saida():
    ref = color_sensor.reflection(PORTA_COR)
    return ref is not None and ref < 20

async def resolver_labirinto():
    print("Aguardando acionamento do sensor de toque para iniciar...")
    while not force_sensor.pressed(PORTA_TOQUE):
        await runloop.sleep_ms(50)

    print("Partida acionada! Navegando no labirinto...")

    motor.run_to_relative_position(PORTA_TORRE, 0, 400)
    await runloop.sleep_ms(400)

    await avancar_uma_celula()

    while True:
        if await detectou_saida():
            motor_pair.stop(motor_pair.PAIR_1)
            print("Saida preta detectada! Labirinto concluido.")
            break

        dist_direita, dist_frente, dist_esquerda = await realizar_varredura()

        parede_direita = dist_direita < LIMIAR_PAREDE_MM
        parede_frente = dist_frente < LIMIAR_PAREDE_MM
        parede_esquerda = dist_esquerda < LIMIAR_PAREDE_MM

        if not parede_direita:
            await virar_angulo(90)
            await avancar_uma_celula()
        elif not parede_frente:
            await avancar_uma_celula()
        elif not parede_esquerda:
            await virar_angulo(-90)
            await avancar_uma_celula()
        else:
            await virar_angulo(179)
            await avancar_uma_celula()

        await runloop.sleep_ms(50)

async def main():
    await resolver_labirinto()

runloop.run(main())
