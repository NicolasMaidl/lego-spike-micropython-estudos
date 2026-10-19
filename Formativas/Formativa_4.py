from hub import port
import motor_pair, color_sensor, runloop
motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

async def pid_seguidor_linha():
    integral = 0
    anteriorErro = 0
    vel = 350
    
    while True:
        erro = 65 - color_sensor.reflection(port.E)
        P_fix = erro * 1.1
        integral = integral + erro
        I_fix = integral * 0.0012
        derivada = erro - anteriorErro
        anteriorErro = erro
        D_fix = derivada * 8

        correcao = min(100, max(-100, int(P_fix + I_fix + D_fix)))
        motor_pair.move(motor_pair.PAIR_1, correcao, velocity = vel)
        await valor_erro()

async def valor_erro():
    print(erro)

async def main():
    await pid_seguidor_linha()
runloop.run(main())
