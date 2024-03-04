import pygame as pg
from settings import *
import load

class Player(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, surface: pg.Surface) -> None:
        super().__init__()
        self.display_surface = surface

        self.load_player_assets()
        self.load_particle_assets()
        self.animation_state = 'idle'
        self.animation_frame = 0
        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect(topleft = pos)

        self.current_hp = PLAYER_HEALTH
        self.max_hp = PLAYER_MAX_HEALTH

        self.velocity = pg.Vector2(0, 0)
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

    def load_player_assets(self) -> None:
        filepath = './assets/player/blue/'
        self.animations = {'idle': [], 'sneak': [], 'walk': [], 'sprint': [], 'airborne': [], 'jump': [], 'land': [], 'hurt': []}
        for animation in self.animations.keys():
            self.animations[animation] = load.import_tilesheet(filepath + 'blue_' + animation + '.png')
    
    def load_particle_assets(self) -> None:
        self.particles_walk = load.import_tilesheet('./assets/player/walk_dust.png')

    def get_input(self) -> None:
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

    def apply_gravity(self) -> None:
        self.velocity.y += min(self.gravity, self.terminal_velocity)
        self.rect.y += self.velocity.y
        if self.jump_cooldown > -1:
            self.jump_cooldown -= 1

    def can_jump(self) -> None:
        return (self.on_ground or self.jumps > 0) and self.jump_cooldown <= 0

    def jump(self) -> None:
        self.velocity.y = self.jump_speed
        self.jumps -= 1
        self.jump_cooldown = PLAYER_JUMP_COOLDOWN
        self.animation_frame = 0
        if self.animation_state != 'hurt':
            self.animation_state = 'jump'

    def animate(self) -> None:
        self.animation_frame += DEFAULT_ANIMATION_SPEED
        animation = self.animations[self.animation_state]
        if self.animation_state == 'sneak':
            animation_frame = int(self.animation_frame // 2) % len(animation)
        else:
            animation_frame = int(self.animation_frame) % len(animation)
        
        image = animation[int(animation_frame)]
        self.image = image if self.facing_right else pg.transform.flip(image, True, False)

        # if self.on_ground:
        #     if self.on_right:
        #         self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        #     elif self.on_left:
        #         self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        #     else:
        #         self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        # if self.on_ceiling:
        #     if self.on_right:
        #         self.rect = self.image.get_rect(topright = self.rect.topright)
        #     elif self.on_left:
        #         self.rect = self.image.get_rect(topleft = self.rect.topleft)
        #     else:
        #         self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def animate_particles(self) -> None:
        if self.animation_state == 'sprint' and self.on_ground:
            animation_frame = int(self.animation_frame) % len(self.particles_walk)
            particle = self.particles_walk[animation_frame]
            particle_rect = particle.get_rect()
            if self.facing_right:
                self.display_surface.blit(particle,
                                        self.rect.bottomleft - pg.Vector2(0, particle_rect.height))
            else:
                self.display_surface.blit(pg.transform.flip(particle, True, False),
                                        self.rect.bottomright - pg.Vector2(particle_rect.width, particle_rect.height))
    
    def land(self) -> None:
        self.animation_frame = 0
        self.animation_state = 'land'

    def update_animation_state(self) -> None:
        if self.animation_state == 'hurt' and self.animation_frame < len(self.animations['hurt']):
            return
        if self.velocity.y != 0:
            if ((self.animation_state != 'jump' and self.animation_state != 'land')
                or self.animation_frame >= len(self.animations['jump']) - DEFAULT_ANIMATION_SPEED):
                self.animation_state = 'airborne'
        elif self.velocity.x != 0:
            if not self.on_ground:
                self.animation_state = 'airborne'
            elif self.speed_mode == PLAYER_SPRINT_MULTIPLIER:
                self.animation_state = 'sprint'
            elif self.speed_mode == PLAYER_SNEAK_MULTIPLIER:
                self.animation_state = 'sneak'
            else:
                self.animation_state = 'walk'
        else:
            if self.animation_frame >= len(self.animations['land']):
                self.animation_state = 'idle'

    def damage(self) -> None:
        self.current_hp -= 1
        self.animation_frame = 0
        self.animation_state = 'hurt'

    def update(self) -> None:
        self.get_input()
        self.update_animation_state()
        self.animate_particles()
        self.animate()