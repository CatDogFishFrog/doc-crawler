# Drawing with Sprites and SpriteLists
## What’s a Sprite?
Each sprite describes where a game object is & how to draw it. This includes:
  * Where it is in the world
  * Where to find the image data
  * How big the image should be


The rest of this page will explain using the [`SpriteList`](../../api_docs/api/sprite_list.html#arcade.SpriteList "arcade.SpriteList") class to draw sprites to the screen.
## Why SpriteLists?
### They’re How Hardware Works
Graphics hardware is designed to draw groups of objects at the same time. These groups are called **batches**.
Each [`SpriteList`](../../api_docs/api/sprite_list.html#arcade.SpriteList "arcade.SpriteList") automatically translates every [`Sprite`](../../api_docs/api/sprites.html#arcade.Sprite "arcade.Sprite") in it into an optimized batch. It doesn’t matter if a batch has one or hundreds of sprites: it still takes the same amount of time to draw!
This means that using fewer batches helps your game run faster, and that you should avoid trying to draw sprites one at a time.
### They Help Develop Games Faster
Sprite lists do more than just draw. They also have built-in features which save you time & effort, including:
  * Automatically skipping off-screen sprites
  * Collision detection
  * Debug drawing for hit boxes


## Using Sprites and SpriteLists
Let’s get to the example code.
There are 3 steps to drawing sprites with a sprite list:
  1. Create a [`SpriteList`](../../api_docs/api/sprite_list.html#arcade.SpriteList "arcade.SpriteList")
  2. Create & append your [`Sprite`](../../api_docs/api/sprites.html#arcade.Sprite "arcade.Sprite") instance(s) to the list
  3. Call [`draw()`](../../api_docs/api/sprite_list.html#arcade.SpriteList.draw "arcade.SpriteList.draw") on your SpriteList inside an [`on_draw()`](../../api_docs/api/window.html#arcade.Window.on_draw "arcade.Window.on_draw") method


Here’s a minimal example:
sprite_minimal.py

```
 1"""
 2Minimal Sprite Example
 3
 4Draws a single sprite in the middle screen.
 5
 6If Python and Arcade are installed, this example can be run from the command line with:
 7python -m arcade.examples.sprite_minimal
 8"""
 9import arcade
10
11
12class GameView(arcade.View):
13
14    def __init__(self):
15        super().__init__()
16        # 1. Create the SpriteList
17        self.sprites = arcade.SpriteList()
18
19        # 2. Create & append your Sprite instance to the SpriteList
20        self.circle = arcade.Sprite()  # Sprite with the default texture
21        self.circle.position = self.center  # center sprite on screen
22        self.sprites.append(self.circle)  # Append the instance to the SpriteList
23
24    def on_draw(self):
25        # 3. Clear the screen
26        self.clear()
27
28        # 4. Call draw() on the SpriteList inside an on_draw() method
29        self.sprites.draw()
30
31
32def main():
33    """ Main function """
34    # Create a window class. This is what actually shows up on screen
35    window = arcade.Window(1280, 720, "Minimal SPrite Example")
36
37    # Create and setup the GameView
38    game = GameView()
39
40    # Show GameView on screen
41    window.show_view(game)
42
43    # Start the arcade game loop
44    arcade.run()
45
46
47if __name__ == "__main__":
48    main()

```

## Using Images with Sprites
Beginners should see the following to learn more, such as how to load images into sprites:
  * [Arcade’s Sprite examples](../../example_code/index.html#sprite-examples)
  * [Arcade’s Simple Platformer Tutorial](../../tutorials/platform_tutorial/index.html#platformer-tutorial)
  * The [`Sprite`](../../api_docs/api/sprites.html#arcade.Sprite "arcade.Sprite") API documentation


## Viewports, Cameras, and Screens
Intermediate users can move past the limitations of [`arcade.Window`](../../api_docs/api/window.html#arcade.Window "arcade.Window") with the following classes:
  * [`arcade.Camera2D`](../../api_docs/api/camera_2d.html#arcade.Camera2D "arcade.Camera2D") ([examples](../../example_code/index.html#camera-examples)) to control which part of game space is drawn
  * [`arcade.View`](../../api_docs/api/window.html#arcade.View "arcade.View") ([examples](../../example_code/index.html#view-examples)) for start, end, and menu screens


