import pygame
from init_fonts import Font


class Controls:
    def __init__(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count()) if "xbox" in pygame.joystick.Joystick(i).get_name().lower()]
        self.controller_type = [i.get_name() for i in self.joysticks][0] if self.joysticks else "Keyboard"
        self.font = Font(size=15)
        self.obj = {'pressed': [], 'up': False, 'down': False, 'right': False,
                    'left': False, 'space': False, 'zoom': False, 'esc': False,
                    'restart': False}

    def start_rumble(self, duration=1):
        [i.rumble(1.0, 1.0, duration) for i in self.joysticks]

    def stop_rumble(self):
        [i.stop_rumble() for i in self.joysticks]

    def blit_controller_type(self, surface, placement="bottomright"):
        padding = 10
        text = self.font.mago_bold.render(f'Controller: {self.controller_type.replace("Controller", "")}', True, (127, 127, 127))
        # bottomright
        x = surface.get_width() - text.get_width() - padding
        y = surface.get_height() - text.get_height() - padding
        surface.blit(text, (x, y))
        self.blit_instructions(surface)

    def blit_instructions(self, surface):
        if self.joysticks:
            instructions = ['Shoot----------------------------B',
                        'Nos------------------------------Y',
                        'Right----------------D-Pad-Right',
                        'Left-------------------D-Pad-Left',
                        'Up-----------------------D-Pad-Up',
                        'Down-----------------D-Pad-Down',
                        'Pause--------------------(-) Back',
                        'Quit----------------------(-) Back',
                        'Start--------------------(+) Start',
                        'Name--------------------A-Z keys']
        else:
            instructions = ['Shoot-----------------SPACE',
                    'Nos-------------------------Z',
                    'Right-----Right-Arrow-Key',
                    'Left--------Left-Arrow-Key',
                    'Up------------Up-Arrow-Key',
                    'Down------Down-Arrow-Key',
                    'Pause--------------------Esc',
                    'Name--------------A-Z keys']
        padding = 10
        for i, v in enumerate(instructions, 2):
            text = self.font.mago_bold.render(v, True, (127, 127, 127))
            x = surface.get_width() - text.get_width() - padding
            y = surface.get_height() - (text.get_height() * i) - padding
            surface.blit(text, (x, y))

    def update_joysticks(self, event):
        if event.type == pygame.JOYDEVICEADDED:
            self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            self.controller_type = [i.get_name() for i in self.joysticks][0] if self.joysticks else "Keyboard"
        if event.type == pygame.JOYDEVICEREMOVED:
            self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            self.controller_type = [i.get_name() for i in self.joysticks][0] if self.joysticks else "Keyboard"

    def activated_pressed(self, pressed):
        # computer keys pressed
        self.obj['pressed'] = pressed
        if not self.joysticks:
            self.obj['esc'] = True if pressed[pygame.K_ESCAPE] else False
            self.obj['left'] = True if pressed[pygame.K_LEFT] else False
            self.obj['down'] = True if pressed[pygame.K_DOWN] else False
            self.obj['space'] = True if pressed[pygame.K_SPACE] else False
            self.obj['up'] = True if pressed[pygame.K_UP] else False
            self.obj['right'] = True if pressed[pygame.K_RIGHT] else False
            self.obj['zoom'] = True if pressed[pygame.K_z] else False
            self.obj['restart'] = True if pressed[pygame.K_r] else False

    def activated_controler(self, event):
        # xbox controller
        if self.joysticks:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:
                    self.obj['space'] = True
                if event.button == 3:
                    self.obj['zoom'] = True
                if event.button == 6:
                    self.obj['esc'] = True
                if event.button == 7:
                    self.obj['restart'] = True
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 1:
                    self.obj['space'] = False
                if event.button == 3:
                    self.obj['zoom'] = False
                if event.button == 6:
                    self.obj['esc'] = False
                if event.button == 7:
                    self.obj['restart'] = False
            if event.type == pygame.JOYHATMOTION:
                # d pad
                self.obj['right'] = True if event.value == (1, 0) else False
                self.obj['left'] = True if event.value == (-1, 0) else False
                self.obj['up'] = True if event.value == (0, 1) else False
                self.obj['down'] = True if event.value == (0, -1) else False
