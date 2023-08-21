import pygame as pg
from settings import *
import load

class Player(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, surface: pg.Surface):
        super().__init__()
        self.image = pg.image.load('assets/test_direction.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        self.display_surface = surface

        self.load_player_assets()
        self.load_particle_assets()
        self.animation_status = 'idle'
        self.frame_index = 0

        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_MAX_HEALTH

        self.velocity = pg.math.Vector2(0, 0)
        self.speed_mode = PLAYER_WALK_MULTIPLIER
        self.max_momentum = PLAYER_MAX_MOMENTUM
        self.inertia = PLAYER_INERTIA
        self.jump_cooldown = 0
        self.jumps = PLAYER_MAX_JUMPS
        self.jump_speed = PLAYER_JUMP_SPEED
        self.gravity = PLAYER_GRAVITY
        self.terminal_velocity = PLAYER_TERMINAL_VELOCITY

        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def load_player_assets(self):
        filepath = './assets/player/blue/'
        self.animations = {'idle': [], 'sneak': [], 'walk': [], 'sprint': [], 'airborne': [], 'jump': [], 'land': []}
        for animation in self.animations.keys():
            self.animations[animation] = load.import_tilesheet(filepath + 'blue_' + animation + '.png')
    
    def load_particle_assets(self):
        self.particles_walk = load.import_tilesheet('./assets/player/walk_dust.png')

    def get_input(self):
        pressed = pg.key.get_pressed()
        if pressed[KEY_SPRINT]:
            self.speed_mode = PLAYER_SPRINT_MULTIPLIER
        elif pressed[KEY_SNEAK]:
            self.speed_mode = PLAYER_SNEAK_MULTIPLIER
        else:
            self.speed_mode = PLAYER_WALK_MULTIPLIER
        
        if pressed[KEY_RIGHT]:
            self.velocity.x = self.max_momentum * self.speed_mode
            self.facing_right = True
        elif pressed[KEY_LEFT]:
            self.velocity.x = -self.max_momentum * self.speed_mode
            self.facing_right = False
        else:
            if -self.inertia/2 <= self.velocity.x <= self.inertia/2:
                self.velocity.x = 0
            elif self.velocity.x > 0:
                self.velocity.x -= self.inertia
            elif self.velocity.x < 0:
                self.velocity.x += self.inertia

        if pressed[KEY_JUMP] and self.can_jump():
            self.jump()

    def apply_gravity(self):
        self.velocity.y += min(self.gravity, self.terminal_velocity)
        self.rect.y += self.velocity.y
        if self.jump_cooldown > -1:
            self.jump_cooldown -= 1

    def can_jump(self):
        return (self.on_ground or self.jumps > 0) and self.jump_cooldown <= 0

    def jump(self):
        self.velocity.y = self.jump_speed
        self.jumps -= 1
        self.jump_cooldown = PLAYER_JUMP_COOLDOWN
        self.frame_index = 0
        self.animation_status = 'jump'

    def animate(self):
        self.frame_index += DEFAULT_ANIMATION_SPEED
        animation = self.animations[self.animation_status]
        if self.animation_status == 'sneak':
            frame_index = int(self.frame_index // 2) % len(animation)
        else:
            frame_index = int(self.frame_index) % len(animation)
        
        image = animation[int(frame_index)]
        self.image = image if self.facing_right else pg.transform.flip(image, True, False)

        if self.on_ground:
            if self.on_right:
                self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
            elif self.on_left:
                self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            else:
                self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        if self.on_ceiling:
            if self.on_right:
                self.rect = self.image.get_rect(topright = self.rect.topright)
            elif self.on_left:
                self.rect = self.image.get_rect(topleft = self.rect.topleft)
            else:
                self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def animate_particles(self):
        if self.animation_status == 'sprint' and self.on_ground:
            frame_index = int(self.frame_index) % len(self.particles_walk)
            particle = self.particles_walk[frame_index]
            particle_rect = particle.get_rect()
            if self.facing_right:
                self.display_surface.blit(particle,
                                        self.rect.bottomleft - pg.math.Vector2(0, particle_rect.height))
            else:
                self.display_surface.blit(pg.transform.flip(particle, True, False),
                                        self.rect.bottomright - pg.math.Vector2(particle_rect.width, particle_rect.height))
    
    def land(self):
        self.frame_index = 0
        self.animation_status = 'land'

    def update_animation_status(self):
        print(self.animation_status, self.frame_index)
        if self.velocity.y != 0:
            if ((self.animation_status != 'jump' and self.animation_status != 'land')
                or self.frame_index >= len(self.animations['jump'])):
                self.animation_status = 'airborne'
        elif self.velocity.x != 0:
            if self.speed_mode == PLAYER_SPRINT_MULTIPLIER:
                self.animation_status = 'sprint'
            elif self.speed_mode == PLAYER_SNEAK_MULTIPLIER:
                self.animation_status = 'sneak'
            else:
                self.animation_status = 'walk'
        else:
            if self.frame_index >= len(self.animations['land']):
                self.animation_status = 'idle'

    def damage(self):
        pass

    def update(self):
        self.get_input()
        self.update_animation_status()
        self.animate_particles()
        self.animate()