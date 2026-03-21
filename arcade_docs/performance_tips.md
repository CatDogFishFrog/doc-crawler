# Performance
[![../_images/flame-arrow.svg](../_images/flame-arrow.svg) ](../_images/flame-arrow.svg)
This page covers the most common slowdowns in games:
  1. [Collision detection](#collision-detection-performance)
  2. [Drawing](#drawing-performance)
  3. [Loading-related issues](#loading-performance)


## Collision Detection Performance
[![../_images/collision.svg](../_images/collision.svg) ](../_images/collision.svg)
### Why are collisions slow?
Imagine you have 50,000 [`Sprite`](../api_docs/api/sprites.html#arcade.Sprite "arcade.Sprite") instances:
  * One is the player
  * The other 49,999 are the ground


#### The Simplest Solutions are Slow
The simplest approach is a for loop over every wall. Even if the hitboxes of both the player and the ground [`Sprite`](../api_docs/api/sprites.html#arcade.Sprite "arcade.Sprite") objects are squares, it will still be a lot of work.
Game developers often use **Big O** notation to describe: * the worst-case execution speed of code * how quickly it grows with the size of the input.
In this case, it grows linearly with the number of walls. Therefore, it’s called “Order N” or “O(N)” and Pronounced “Oh-En”.
Adding more moving elements means the number of collision checks will grow very quickly. How do we stop a game from dropping below 60 FPS?
### The Faster Alternatives
Arcade supports two solutions out the box. Both are described below:
  1. The built-in [Spatial Hashing](#collision-detection-performance-hashing)
  2. The [Pymunk physics engine integrations](#collision-detection-performance-pymunk)


#### Which should I use?  
| Approach  | Best when  | Example code  |  
| --- | --- | --- |  
| Default settings  | N < 100 sprites (especially if most move)  | [Sprites That Follow The Player](../example_code/sprite_follow_simple.html#sprite-follow-simple)  |  
| Spatial hashing  | N > 100 mostly non-moving sprites [[1]](#id4)  | [Line of Sight](../example_code/line_of_sight.html#line-of-sight)  |  
| [`PymunkPhysicsEngine`](../api_docs/api/physics_engines.html#arcade.PymunkPhysicsEngine "arcade.pymunk_physics_engine.PymunkPhysicsEngine")  | You need forces, torque, joints, or springs  | [Using PyMunk for Physics](../example_code/index.html#example-code-pymunk)  |  
### Spatial Hashing
**Spatial hashing** is meant for collision checking sprites against a [`SpriteList`](../api_docs/api/sprite_list.html#arcade.SpriteList "arcade.SpriteList") of **non-moving** sprites:
  * checking collisions against hashed sprites becomes much faster
  * moving or resizing any sprite in the hash becomes much slower


It divides the game world into grid squares of regular size. Then, it uses a **hash map** ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")) of grid square coordinates to lists of [`Sprite`](../api_docs/api/sprites.html#arcade.Sprite "arcade.Sprite") objects in each square.
How does this help us? We may need as few as zero hitbox checks to collide a given sprite against a [`SpriteList`](../api_docs/api/sprite_list.html#arcade.SpriteList "arcade.SpriteList"). Yes, **zero** :
![A blue bird is alone in its own grid square.](../_images/spatial_hash_grid_mockup.png)
  1. The sand-colored ground consists of sprites in a [`SpriteList`](../api_docs/api/sprite_list.html#arcade.SpriteList "arcade.SpriteList") with spatial hashing enabled
  2. The bright green lines show the grid square boundaries
  3. The moving sprites are the blue bird and the red angry faces


The exact number of checks per moving sprite depends on the following:
  * the grid size chosen (controlled by the `spatial_hash_cell_size` argument)
  * how many [`Sprite`](../api_docs/api/sprites.html#arcade.Sprite "arcade.Sprite") objects are in any given square
  * the size of each [`Sprite`](../api_docs/api/sprites.html#arcade.Sprite "arcade.Sprite") passed


Since the bird is small enough to be alone in a grid square, it will perform zero hitbox checks against terrain while flying. This will also be true for any projectiles or other flying objects in the air above the terrain.
What about the red angry-faces on the ground? They still perform fewer hitbox checks against terrain than if spatial hashing was not enabled.
#### Enabling Spatial Hashing
The best way to enable spatial hashing on a [`SpriteList`](../api_docs/api/sprite_list.html#arcade.SpriteList "arcade.SpriteList") is before anything else, especially before gameplay.
The simplest way is passing `use_spatial_hash=True` when creating and storing the list inside a [`Window`](../api_docs/api/window.html#arcade.Window "arcade.Window") or [`View`](../api_docs/api/window.html#arcade.View "arcade.View"):

```
# Inside a Window or View, and often inside a setup() method
self.spritelist_with_hashing = arcade.SpriteList(use_spatial_hash=True)

```

#### Spatial Hashing and Tiled Maps
There is also a way to enable spatial hashing when loading Tiled maps. For each layer you’d like to load with spatial hashing, set a `"use_spatial_hashing"` key in its layer options to `True`:

```
layer_options = {
     "ground": {
         "use_spatial_hash": True
     },
     "non_moving_platforms": {
         "use_spatial_hash": True
     }
}

```

For a runnable example of this, please see [Camera Use in a Platformer](../example_code/camera_platform.html#camera-platform). Additional examples are linked below in [Further Example Code](#collision-performance-spatial-hashing-examples).
#### The Catch
Spatial hashing doubles the cost of moving or resizing sprites.
However, this doesn’t mean we can’t _ever_ move or resize a sprite! Instead, it means we have to be careful about when and how much we do so. This is because moving and resizing now consists of:
  1. Remove it from the internal list of every grid square it is currently in
  2. Add it again by re-computing its new location


If we only move a few sprites in the list now and then, it can work out. When in doubt, test it and see if it works for your specific use case.
#### Further Example Code
For detailed step-by-step tutorial steps on using spatial hashing, please see:
  * [Step 3 - Many Sprites with SpriteList](../tutorials/platform_tutorial/step_03.html#platformer-part-three)
  * [Step 12 - Loading a Map From a Map Editor](../tutorials/platform_tutorial/step_12.html#platformer-part-twelve)


For detailed API notes, please see:
  * [`arcade.SpriteList`](../api_docs/api/sprite_list.html#arcade.SpriteList "arcade.SpriteList")
  * [`arcade.SpriteList.enable_spatial_hashing()`](../api_docs/api/sprite_list.html#arcade.SpriteList.enable_spatial_hashing "arcade.SpriteList.enable_spatial_hashing")
  * [`arcade.sprite_list.spatial_hash.SpatialHash`](../api_docs/api/sprite_list.html#arcade.SpatialHash "arcade.sprite_list.spatial_hash.SpatialHash")
  * [`arcade.physics_engines.PhysicsEngineSimple`](../api_docs/api/physics_engines.html#arcade.PhysicsEngineSimple "arcade.physics_engines.PhysicsEngineSimple")
  * [`arcade.physics_engines.PhysicsEnginePlatformer`](../api_docs/api/physics_engines.html#arcade.PhysicsEnginePlatformer "arcade.physics_engines.PhysicsEnginePlatformer")


#### Spatial Hashing Implementation Details
Note
Many readers can skip this section.
The hash map is a Python [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)") mapping [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "\(in Python v3.14\)") coordinate pairs to [`list`](https://docs.python.org/3/library/stdtypes.html#list "\(in Python v3.14\)") instances.
“Hashing” works like this for any given sprite:
  1. Divide the X and Y of its lower left by the grid square size
  2. Divide the X and Y of its upper right by the grid square size
  3. Every grid square between these is considered touched


Adding a sprite hashes its hitbox as above. Colliding with sprites already added involves hashing, then performing a detailed collision check against every sprite in every touched tile.
### Pymunk Physics Engine
Arcade provides a helper wrappers around [Pymunk](https://www.pymunk.org/en/latest/index.html), a binding for the professional-grade [Chipmunk2D](https://chipmunk-physics.net/) engine.
It offers many features beyond anything Arcade’s other built-in physics options currently offer. This professional-grade power comes with complexity and speed many users may want find worthwhile.
None of Arcade’s other engines support torque, multiple forces, joints, or springs. If you find yourself needing these or the speed only binary-backed acceleration can offer, this may be the right choice.
To get started, please see the following:
  * The [Using PyMunk for Physics](../example_code/index.html#example-code-pymunk) Example
  * Arcade’s [Pymunk Platformer](../tutorials/pymunk_platformer/index.html#pymunk-platformer-tutorial) tutorial
  * [`arcade.pymunk_physics_engine.PymunkPhysicsEngine`](../api_docs/api/physics_engines.html#arcade.PymunkPhysicsEngine "arcade.pymunk_physics_engine.PymunkPhysicsEngine")
  * The [`pymunk`](https://www.pymunk.org/en/latest/pymunk.html#module-pymunk "\(in Pymunk\)") documentation


### Compute Shader
Currently on the drawing board, is the use of a **compute shader** on your graphics card to detect collisions. This has the speed advantages of spatial hashing, without the speed penalty.
## Drawing Performance
To draw at 60 frames per second or better, there are rules you need to follow.
The most important is simple. You should draw items the same way you would bake muffins: in batches. If you ignore this, you will have poor drawing performance.
The rest of this section will cover how to avoid that.
### Drawing Shapes
The `arcade.draw_*` functions are slow despite being convenient.
This is because it does not perform batched drawing. Instead of sending batches of shapes to draw, it sends them individually.
You have three options for drawing shapes more efficiently:
  1. Use Arcade’s non-modifiable shapes with [`arcade.shape_list.ShapeElementList`](../api_docs/api/drawing_batch.html#arcade.shape_list.ShapeElementList "arcade.shape_list.ShapeElementList")
  2. Use pyglet’s updatable [`pyglet.shapes`](https://pyglet.readthedocs.io/en/latest/modules/shapes.html#module-pyglet.shapes "\(in pyglet v2.1\)") module
  3. Write your own advanced shaders


For more information, please see:
  * [ShapeElementList Explanation](../example_code/shape_list_demo.html#shape-list-demo)


## Sprite drawing performance
Arcade’s [`arcade.SpriteList`](../api_docs/api/sprite_list.html#arcade.SpriteList "arcade.SpriteList") is the only way to draw a [`Sprite`](../api_docs/api/sprites.html#arcade.Sprite "arcade.Sprite").
This is because all drawing with a graphics card is batched drawing. The [`SpriteList`](../api_docs/api/sprite_list.html#arcade.SpriteList "arcade.SpriteList") handles batching for you. As a result, you can draw thousands of moving sprites with any extra effort on your part.
### An Option for Advanced Users
Advanced users may want to try pyglet’s [`pyglet.sprite.Sprite`](https://pyglet.readthedocs.io/en/latest/modules/sprite.html#pyglet.sprite.Sprite "\(in pyglet v2.1\)").
Instead of Arcade’s [`SpriteList`](../api_docs/api/sprite_list.html#arcade.SpriteList "arcade.SpriteList"), pyglet sprites use a mix of the following classes:
  * [`pyglet.graphics.Batch`](https://pyglet.readthedocs.io/en/latest/modules/graphics/index.html#pyglet.graphics.Batch "\(in pyglet v2.1\)")
  * [`pyglet.graphics.Group`](https://pyglet.readthedocs.io/en/latest/modules/graphics/index.html#pyglet.graphics.Group "\(in pyglet v2.1\)")


Both pyglet’s sprites, groups, and batches are much closer to OpenGL’s low-level components and will require investing time to learn their features. They also lack many of the features you may be used to in Arcade.
## Text drawing performance
The slowest thing aside from disk access is [`arcade.draw_text()`](../api_docs/api/text.html#arcade.draw_text "arcade.draw_text").
To improve performance:
  1. Use [`arcade.Text`](../api_docs/api/text.html#arcade.Text "arcade.Text") instead
  2. (Optional) Pass a pyglet [`Batch`](https://pyglet.readthedocs.io/en/latest/modules/graphics/index.html#pyglet.graphics.Batch "\(in pyglet v2.1\)") object at creation


See the following to learn more:
  * [Better Text Drawing with Text Objects](../example_code/drawing_text_objects.html#drawing-text-objects)
  * [The Fastest Text Drawing: pyglet Batches](../example_code/drawing_text_objects_batch.html#drawing-text-objects-batch)


## Loading Performance
Disk access is one of the slowest things a computer can do.
Your goal for minimizing performance is to reduce the amount of data you read and write during gameplay to a minimum. Fortunately, this is fairly easy. It comes down to one thing above all else.
Preload everything you can before gameplay.
### Loading Screens and Rooms
You may be familiar with loading screens.
Other approaches include:
  * In-game loading “rooms” with minimal performance impact
  * Multi-threading to load data on background threads [[2]](#id8)


Both allow background loading of data before gameplay. You can use these for loading audio, textures, and other data before the player enters the game.
However, there are a few exceptions. These are described below, especially with streaming audio.
## Sound Performance in Depth
This page covers static and streaming sounds in depth.
If you are not familiar, you may want to read [Streaming or Static Loading?](sound.html#sound-loading-modes) before proceeding.
### Static Sounds are for Speed
Static sounds can help your game run smoothly by preloading data before gameplay.
If music is a central part of your gameplay or application, then in some cases you may want to use this approach for loading music. However, you should be careful about it.
Each decompressed minute of CD-quality audio uses slightly over 10 MB of RAM. This adds up quickly. Loading entire albums into memory without clearing them can slow down or freeze a computer, especially if you fill RAM completely.
For music and long background audio, you should strongly consider [streaming](#sound-loading-modes-streaming) from compressed files instead.
#### When to Use Static Sounds
If an audio file meets one or more of the following conditions, you may want to load it as static audio:
  * You need to start playback quickly in response to gameplay.
  * Two or more “copies” of the sound can be playing at the same time.
  * You will unpredictably skip to different times in the file.
  * You will unpredictably restart playback.
  * You need to automatically loop playback.
  * The file is a short clip.


### Streaming Saves Memory
Streaming audio from compressed files is similar to streaming video online.
Both save memory by:
  1. Transmitting a compressed version over a constrained connection
  2. Only decompressing part of a file in memory at a time


As with online video, this works on even the weakest recent hardware if:
  * You only stream one media source at a time.
  * You don’t need to loop or jump around in the audio.


Since compressed formats like MP3 are much smaller than their decompressed forms, the cost of reading them piece by piece into RAM can be an acceptable tradeoff which saves memory. Once in RAM, many formats are quick to decompress and worth the RAM savings.
#### When to Stream
In general, avoid streaming things other than music and ambiance.
In addition to disabling features like looping and multiple playbacks, they can also introduce other complications. For example, you may face issues with synchronization and interruptions. These may worsen as the quantity and quality of the audio tracks involved increases.
If you’re unsure, avoid streaming unless you can say yes to all of the following:
  1. The [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.sound.Sound") will have at most one playback at a time.
  2. The file is long enough to make it worth it.
  3. Seeking (skipping to different parts) will be infrequent.
     * Ideally, you will never seek or restart playback suddenly.
     * If you do seek, the jumps will ideally be close enough to land in the same or next chunk.


See the following to learn more:
  * [Change Ongoing Playbacks via Player Objects](sound.html#sound-intermediate-playback-change-aspects-ongoing)
  * The [`pyglet.media.StreamingSource`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.StreamingSource "\(in pyglet v2.1\)") class used to implement streaming


#### Streaming Can Cause Freezes
Failing to meet the requirements above can cause buffering issues.
Good compression on files can help, but it can’t fully overcome it. Each skip outside the currently loaded data requires reading and decompressing a replacement.
In the worst-case scenario, frequent skipping will mean constantly buffering instead of playing. Although video streaming sites can downgrade quality, your game will be at risk of stuttering or freezing.
The best way to handle this is to only use streaming when necessary.
