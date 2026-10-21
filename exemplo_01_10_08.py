from hub import light_matrix,port,sound
import color,color_sensor, runloop, motor, force_sensor, time
def piscar():
    light_matrix.show_image(light_matrix.IMAGE_ARROW_N)
    time.sleep_ms(500)
    light_matrix.show_image(light_matrix.IMAGE_ARROW_S)
    time.sleep_ms(500)
    light_matrix.show_image(light_matrix.IMAGE_ARROW_E)
    time.sleep_ms(500)        
    light_matrix.show_image(light_matrix.IMAGE_ARROW_W)
    time.sleep_ms(500)    
def motoresJuntos():
    motor.run_for_degrees(port.A,360,720)          #girar os dois motores JUNTOS a 360 graus a 720 graus por segundo
    motor.run_for_degrees(port.C,360,720)
async def motoresSeparados():
    await motor.run_for_degrees(port.A,360,720)    #girar os dois motores SEPARADAMENTE a 360 graus a 720 graus por segundo
    await motor.run_for_degrees(port.C,360,720)
def motorSensor():
    forca = force_sensor.force(port.D)
    return forca
async def main():
    if color_sensor.color(port.B) == color.RED:
        print("Hello World!!!!!!!!")    
    piscar()
    motoresJuntos()
    time.sleep_ms(1000)
    await motoresSeparados()
    time.sleep_ms(1000)
    motorSensor()
    print(motorSensor())                           #mostra o valor da forca na tela
    motor.run(port.A,motorSensor())                #atribui essa forca ao motor 
    await sound.beep(1040,10000,100)
    motor.stop(port.A)

runloop.run(main())
