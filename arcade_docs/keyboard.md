# Keyboard
## Events
### What is a keyboard event?
Keyboard events are Arcade’s representation of physical keyboard interactions.
For example, if your keyboard is working correctly and you type the letter A into the window of a running Arcade game, it will see two separate events:
  1. a key press event with the key code for `A`
  2. a key release event with the key code for `A`


### How do I handle keyboard events?
You must implement key event handlers. These functions are called whenever a key event is detected:
  * [`arcade.Window.on_key_press()`](../api_docs/api/window.html#arcade.Window.on_key_press "arcade.Window.on_key_press")
  * [`arcade.Window.on_key_release()`](../api_docs/api/window.html#arcade.Window.on_key_release "arcade.Window.on_key_release")


You need to implement your own versions of the above methods on your subclass of [`arcade.Window`](../api_docs/api/window.html#arcade.Window "arcade.Window"). The [arcade.key](../api_docs/arcade.key.html#key) module contains constants for specific keys.
For runnable examples, see the following:
  * [Move By Keyboard](../example_code/sprite_move_keyboard.html#sprite-move-keyboard)
  * [Better Move By Keyboard](../example_code/sprite_move_keyboard_better.html#sprite-move-keyboard-better)
  * [Acceleration and Friction](../example_code/sprite_move_keyboard_accel.html#sprite-move-keyboard-accel)


Note
If you are using [`Views`](../api_docs/api/window.html#arcade.View "arcade.View"), you can also implement key event handler methods on them.
## Modifiers
### What is a modifier?
Modifiers are keys that modify the behavior of keyboard input. Examples include keys such as shift, control, and command. Lock keys such as capslock are also modifiers.
### What does active mean?
Modifiers can be active in two ways:
  1. A modifier key is currently held down by the user (example: shift)
  2. A lock modifier is currently turned on (example: capslock)


This is important because lock modifiers can be active without their corresponding key held down. Instead, they are switched on and off by pressing their keys.
### How do I use modifiers?
As long as you don’t need to distinguish between the left and right versions of modifiers keys, you can rely on the `modifiers` argument of [key event handlers](#keyboard-event-handlers).
For every key event, the current state of all modifiers is passed to the handler method through the `modifiers` argument as a single integer. For each active modifier during an event, a corresponding bit is set to 1.
Constants for each of these bits are defined in [arcade.key](../api_docs/arcade.key.html#key):

```
MOD_SHIFT
MOD_CTRL
MOD_ALT         Not available on Mac OS X
MOD_WINDOWS     Available on Windows only
MOD_COMMAND     Available on Mac OS X only
MOD_OPTION      Available on Mac OS X only
MOD_CAPSLOCK
MOD_NUMLOCK
MOD_SCROLLLOCK
MOD_ACCEL       Equivalent to MOD_CTRL, or MOD_COMMAND on Mac OS X.

```

You can use these constants with bitwise operations to check if a specific modifier is active during a keyboard event:

```
# this should be implemented on a subclass of Window or View
def on_key_press(self, symbol, modifiers):

    if modifiers & arcade.key.MOD_SHIFT:
        print("The shift key is held down")

    if modifiers & arcade.key.MOD_CAPSLOCK:
        print("Capslock is on")

```

### How do I tell left & right modifers apart?
Many keyboards have both left and right versions of modifiers such as shift and control. However, the `modifiers` argument to key handlers does not tell you which specific modifier keys are currently pressed!
Instead, you have to use specific key codes for left and right versions from [arcade.key](../api_docs/arcade.key.html#key) to [track press and release events](#keyboard-event-handlers).
