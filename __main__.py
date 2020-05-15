# coding=utf-8

import fractal
import screen_pg
import event_pg
import time

spg = screen_pg.ScreenPg()
epg = event_pg.EventPg(spg.pg)
spg.beggin()
spg.set_title('Cellular Automata: Fractal')

fr = fractal.Fractal(width = spg.width, height = spg.height)

def reset():
    fr.reset_game_state()
    spg.screen.fill(spg.bg)

# rule = 110
# rule = 124
# rule = 150
# rule = 90

# Para regla 110
# gameState[nxC -1 , 0] = 1
# Para regla 124
# gameState[0, 0] = 1

init_config = {
    'sleep': 0.01,
    # Control de la ejecución del juego.
    'pauseExec': False,
    # Para seguir calculando y pintando al reanudar.
    'painted': False,
    'auxX': 0,
    'auxY': 0,
    'x': 0,
    'y': 0
    }

config = init_config.copy()

def info():
    return ["  -- INFO --",
            "  ==========",
            "    rule:    #{}".format(fr.rule),
            "    rows:     {}".format(fr.nyC),
            "    columns:  {}".format(fr.nxC),
            "    width     {}".format(spg.width),
            "    height:   {}".format(spg.height),
            "  ==========",
            "  -- MAN --",
            "  ==========",
            "  [M+,m-] 10 in rule",
            "  [N+,n-] 1 in rule",
            "  [LEFT-] 10 columns",
            "  [RIGHT+] 10 columns",
            "  [UP] 10 rows",
            "  [DOWN] 10 rows",
            "  [SPACE] pause",
            "  [ESC] exit"]

def do_painted():
    # Detenemos la ejecución si ya se terminó de pintar.
    if config['y'] == fr.nyC:
        config['painted'] = True

def do_exit(ev):
    if epg.event_close(ev):
        spg.quit()
        exit()

def do_listened(ev, config):
    if epg.listen(ev, fr, spg):
        reset()
        return init_config.copy()
    return config

font = spg.pg.font.SysFont('comicsansms', 16)

# Bucle de ejecición.
from sys import exit
while  config['y']< fr.nyC or spg.running:
    text = info()
    str_rule = []
    for line in text:
        str_rule.append(font.render(line, True, (255, 255, 255)))

    restart = False
    do_painted()

    # Registramos eventos de teclado y ratón.
    ev = epg.get_event()
    do_exit(ev)

    config = do_listened(ev, config)

    if not config['painted'] or not restart:
        epg.pause_exec(ev, config)
        if not config['pauseExec']:
            # time.sleep(config['sleep'])
            for config['x'] in range(0, fr.nxC):
                if fr.cal_cell(config['x'], config['y']):
                    fr.cell_born(config['x'], config['y'])
                    spg.draw_polygon((31, 184, 163), fr.polygon(config['x'], config['y']))
            spg.update()
            config['y'] += 1

    spg.pg.draw.rect(spg.screen, (0, 0, 0), [0, 0, 180, 22 * len(text)], 0)
    for line in range(len(str_rule)):
        spg.screen.blit(str_rule[line], (0, line * 21))
    spg.update()

