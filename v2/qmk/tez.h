#pragma once

#ifdef KEYBOARD_tez_rev1
    #include "rev1.h"
#endif

#include "quantum.h"

#define KC_LSHIFT KC_LEFT_SHIFT	
#define KC_RSHIFT KC_RIGHT_SHIFT	
#define KC_LCTRL KC_LEFT_CTRL	
#define KC_RCTRL KC_RIGHT_CTRL	
#define KC_PGDOWN KC_PAGE_DOWN
#define KC_PGUP KC_PAGE_UP

#define KC_LBRACKET KC_LEFT_BRACKET
#define KC_RBRACKET KC_RIGHT_BRACKET
#define KC_SCOLON KC_SEMICOLON
#define KC_BSPACE KC_BACKSPACE
#define KC_PC_CUT KC_CUT
#define KC_PC_COPY KC_COPY
#define KC_PC_PASTE KC_PASTE
#define KC_NUMLOCK KC_NUM_LOCK
#define KC_BSLASH KC_BACKSLASH
#define KC_PC_UNDO KC_UNDO

#define KC_CH_LNG LALT(KC_LSHIFT)

#define KC_COPY LCTL(KC_C)
#define KC_PASTE LCTL(KC_V)
#define KC_CUT LCTL(KC_X)
#define KC_M_ALL LCTL(KC_A)
