import pygame
from projectile import Projectile

class EffectProjectile(Projectile):
    def __init__(self, pos, direction, speed, lifespan, effect_type="blue_orb", damage=10, weapon_type="effect"):
        # Load the effect sprite sheet
        self.effect_sheet = pygame.image.load("assets/sprites/effects/blue_effects.png").convert_alpha()
        
        self.effect_properties = {
            "ice_flame": {
                "row": 0,
                "frames": 3,
                "size": (16, 16),
                "animation_speed": 15
            },
            "ice_kunai": {
                "row": 4,
                "frames": 3,
                "size": (16, 16),
                "animation_speed": 3
            },
            "ice_spark": {
                "row": 7,
                "frames": 3,
                "size": (16, 16),
                "animation_speed": 15
            },
            
            # Effects starting at column 10
            "fading_fire": {
                "row": 0,
                "frames": 3,
                "size": (16, 16),
                "animation_speed": 2,
                "start_col": 10
            },
            "hadouken": {
                "row": 1,
                "frames": 2,
                "size": (16, 16),
                "animation_speed": 15,
                "start_col": 10
            },
            "blue_orb": {
                "row": 7,
                "frames": 3,
                "size": (16, 16),
                "animation_speed": 15,
                "start_col": 10
            },
            
            # Multi-row effects
            "large_blue_orb": {
                "row": 1,
                "frames": 4,
                "size": (16, 32),  # Double height
                "animation_speed": 15,
                "multi_row": True,
                "start_col": 10
            },
            "large_fire_orb": {
                "row": 10,
                "frames": 3,
                "size": (16, 32),  # Double height
                "animation_speed": 15,
                "multi_row": True,
                "start_col": 10
            }
        }
        
        # Get properties for the selected effect
        props = self.effect_properties[effect_type]
        
        # Load the first frame as the initial image
        initial_frame = self.load_frame(props["row"], 0, props["size"], props.get("start_col", 0), props.get("multi_row", False))
        
        # Initialize the base projectile with the first frame
        super().__init__(pos, direction, speed, lifespan, initial_frame, damage, weapon_type)
        
        # Animation properties
        self.effect_type = effect_type
        self.frame_index = 0
        self.animation_speed = props["animation_speed"]
        self.frames = props["frames"]
        self.frame_size = props["size"]
        self.start_col = props.get("start_col", 0)
        self.start_row = props.get("start_row", 0)
        self.multi_row = props.get("multi_row", False)
        
        # Load all frames for this effect
        self.animation_frames = [
            self.load_frame(props["row"], i, props["size"], self.start_col, self.multi_row)
            for i in range(props["frames"])
        ]

    def load_frame(self, row, frame_index, size, start_col=0, multi_row=False):
        """Load a single frame from the sprite sheet."""
        x = (start_col + frame_index) * size[0]
        y = row * size[1]
        
        if multi_row:
            # For multi-row effects, combine two rows
            frame1 = self.effect_sheet.subsurface(pygame.Rect(x, y, size[0], size[1]//2))
            frame2 = self.effect_sheet.subsurface(pygame.Rect(x, y + size[1]//2, size[0], size[1]//2))
            
            # Create a new surface to combine the frames
            combined_frame = pygame.Surface(size, pygame.SRCALPHA)
            combined_frame.blit(frame1, (0, 0))
            combined_frame.blit(frame2, (0, size[1]//2))
            return combined_frame
        else:
            rect = pygame.Rect(x, y, size[0], size[1])
            return self.effect_sheet.subsurface(rect)

    def update(self, dt):
        # Update animation
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= self.frames:
            self.frame_index = 0
        
        # Update the current frame
        self.image = self.animation_frames[int(self.frame_index)]
        
        # Call the parent class update method
        super().update(dt) 