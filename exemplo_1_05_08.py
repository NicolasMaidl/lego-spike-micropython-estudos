from hub import light_matrix,sound
import runloop, time

async def main():
    while True:
        await light_matrix.write("Hi!")
        sound.beep(440,1000,100)
        light_matrix.show_image(light_matrix.IMAGE_HAPPY)
        time.sleep_ms(500)

runloop.run(main())
