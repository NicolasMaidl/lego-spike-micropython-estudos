from hub import port
import runloop, distance_sensor,motor_pair,force_sensor,color_sensor,color
def obstaculo():
    d = distance_sensor.distance(port.F)
    return d>0 and d<50
def toque():
    return force_sensor.pressed(port.B)
def encontraCor():
    return color_sensor.color(port.A) == color.BLACK
async def main():
    motor_pair.pair(motor_pair.PAIR_1,port.C,port.D)
    motor_pair.move(motor_pair.PAIR_1,0)
    await runloop.until(obstaculo)
    print("Obstáculo encontrado!!!")
    await runloop.until(toque)
    print("Toque pressionado!!!")
    await runloop.until(encontraCor)
    print("Cor BLACK encontrada!!!")
    motor_pair.stop(motor_pair.PAIR_1)
runloop.run(main())
