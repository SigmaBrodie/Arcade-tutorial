import arcade
import os
# Constants
 # Width of the screen
SCREEN_WIDTH = 1000 
# Height of the screen
SCREEN_HEIGHT = 650 
# Title of the game window
SCREEN_TITLE = "Platformer"  
# Scaling factor for character sprites
CHARACTER_SCALING = 1 
# Scaling factor for tile sprites 
TILE_SCALING = 0.5  
# Movement speed of the player (pixels per frame)
PLAYER_MOVEMENT_SPEED = 5 
# Gravity constant 
GRAVITY = 1  
# Speed of player's jump
PLAYER_JUMP_SPEED = 20  

# Main game class
class MyGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """Initialize the game window."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our TileMap Object
        self.tile_map = None
        # Scene object
        self.scene = None  
        # Player sprite
        self.player_sprite = None  
        # Physics engine
        self.physics_engine = None  
        # Camera for scrolling
        self.camera = None  

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game."""

        # Set path to start this program
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)


        # Initialize camera
        self.camera = arcade.Camera(self.width, self.height)  

        map_name = ("./sigmamap1.tmx")



        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        

        # Add sprite list for player
        self.scene.add_sprite_list("Player")  
        # Add sprite list for walls
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)  

        # Create and position the player sprite
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 300
        self.scene.add_sprite("Player", self.player_sprite)


        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Tile Layer 1"]
        )



        

    def on_draw(self):
        """Render the screen."""
        self.clear()
        # Activate the camera
        self.camera.use() 
        # Draw the scene
        self.scene.draw() 

    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Handle key release events."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        """Center the camera on the player."""
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Ensure camera doesn't travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Update game logic."""
        # Update physics engine
        self.physics_engine.update()  
        # Position the camera
        self.center_camera_to_player()  


def main():
    """Main function."""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()