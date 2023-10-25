/*
Copyright 2019 Tom Saleeba <ergoslab@techotom.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#pragma once

// wiring of each half
#define MATRIX_ROW_PINS { D4, C6, D7, E6 }
#define MATRIX_COL_PINS { B4, B5, B6, B3, B2 }
 // #define MATRIX_COL_PINS { B4, B5, B6, B2, B3 }
#define MATRIX_COL_PINS_RIGHT { B4, B5, B6, B2, B3 }

/* COL2ROW or ROW2COL */
// #define DIODE_DIRECTION COL2ROW
#define DIODE_DIRECTION ROW2COL

/* ws2812 RGB LED */
#define RGB_DI_PIN B1

#define RGBLED_NUM 12    // Number of LEDs
// FIXME this following line should enable our layer status LEDs to work on both
// sides without need to wire them into a chain. It doesn't though. Uncommenting
// means the slave side of the keyboard stops working (and the LEDs don't work).
#define RGBLED_SPLIT {6,6}
#define RGBLIGHT_LAYERS
#define RGBLIGHT_EFFECT_BREATHING
#define RGBLIGHT_EFFECT_KNIGHT
#define RGBLIGHT_EFFECT_RAINBOW_MOOD
// #define RGBLIGHT_DEFAULT_MODE 

/*
 * Feature disable options
 *  These options are also useful to firmware size reduction.
 */

/* disable debug print */
// #define NO_DEBUG

/* disable print */
// #define NO_PRINT

/* disable action features */
//#define NO_ACTION_LAYER
//#define NO_ACTION_TAPPING
//#define NO_ACTION_ONESHOT
// #define SOFT_SERIAL_PIN D2
// #define SERIAL_USART_TX_PIN D2
#define MASTER_LEFT
#define SOFT_SERIAL_PIN D0
#define USE_SERIAL

#define SPLIT_USB_DETECT
#define SPLIT_USB_TIMEOUT 2000

// for keyboard-level data sync:
#define SPLIT_TRANSACTION_IDS_KB KEYBOARD_SYNC_A, KEYBOARD_SYNC_B

/* Tap config */
#define TAPPING_TERM 150
#define IGNORE_MOD_TAP_INTERRUPT

#define DEBOUNCE 5

// [> Mouse Configuration <]
// #define MOUSEKEY_DELAY 2
// #define MOUSEKEY_INTERVAL 30
// // #define MOUSEKEY_INITIAL_SPEED 50
// #define MOUSEKEY_BASE_SPEED 100
