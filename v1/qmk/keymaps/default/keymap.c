/* Copyright 2021 Yehonatan Elentok
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
#include QMK_KEYBOARD_H

// Defines names for use in layer keycodes and the keymap
enum layer_names {
    _BASE,
    _MOVE,
    _NUMPAD,
    _MOUSE_F,
    _SYMBOLS,
    _GAME,
    _GAME_NUM
};

//Home row
#define KC_CTL_A LCTL_T(KC_A)
#define KC_GUI_S LGUI_T(KC_S)
#define KC_SFT_D LSFT_T(KC_D)
#define KC_ALT_Z LALT_T(KC_Z)

//Layers Move
#define KC_LNUM_F LT(_NUMPAD,KC_F)
#define KC_LSYM_F LT(_SYMBOLS,KC_V)
#define KC_LNUM_SP LT(2,KC_SPACE)

#define KC_PC_CUT LCTL(KC_X)
#define KC_TRAN KC_TRANSPARENT

/** enum custom_keycodes { */
/**   RGB_SLD = EZ_SAFE_RANGE, */
/**   ST_MACRO_0, */
/** }; */

// Defines the keycodes used by our macros in process_record_user
enum custom_keycodes {
    QMKBEST = SAFE_RANGE,
    ST_MACRO_0,
};

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    /* Base */
    [_BASE] = LAYOUT(
            KC_Q,           KC_W,                   KC_E,               KC_R, KC_T,                                KC_Y, KC_U, RSFT_T(KC_I), RGUI_T(KC_O), KC_P, 
            LCTL_T(KC_A),   LGUI_T(KC_S),           LSFT_T(KC_D),       LT(_NUMPAD, KC_F), KC_G,                   KC_H, KC_J, KC_K, KC_L, RCTL_T(KC_SCLN), 
            LALT_T(KC_Z),   KC_X, KC_C,             LT(_SYMBOLS, KC_V), KC_B,                                      KC_N, KC_M, KC_COMM, KC_DOT, LT(_MOUSE_F, KC_SLASH), 
                                MO(_MOUSE_F),   LT(_NUMPAD,KC_SPACE),   KC_LSFT,                           KC_BSPC,   LT(_MOVE, KC_ENT), MO(_MOUSE_F)
       ),
    [_MOVE] = LAYOUT(
            KC_BSPC,        KC_TRAN,       KC_LBRACKET,    KC_RBRACKET,    LSFT(KC_TAB),                           KC_HOME,        KC_PGDOWN,      KC_PGUP,        KC_DELETE,      LSFT(KC_F10),
            KC_LCTRL,       KC_TRAN,       KC_LPRN,        KC_RPRN,        KC_TAB,                                 KC_LEFT,        KC_DOWN,        KC_UP,          KC_RIGHT,       KC_RCTRL,
            KC_LALT,        KC_TRAN,       KC_LCBR,        KC_RCBR,        KC_GRAVE,                               KC_END,         KC_INS,         KC_WBAK,        KC_WFWD,        KC_ENTER,
                                                           MO(_MOUSE_F), KC_LNUM_SP, KC_LSHIFT,         KC_BSPACE, LT(_MOVE,KC_ENTER),MO(_MOUSE_F) 
       ),
    [_NUMPAD] = LAYOUT(
            KC_BSPACE,      KC_ESCAPE,     KC_ENTER,       KC_DQUO,        KC_TRAN,                                KC_EQUAL,         KC_7,           RSFT_T(KC_8),   KC_9,           KC_ASTR,
            KC_LCTRL,    KC_LGUI,       KC_LSHIFT,      KC_QUOTE,       LSFT(KC_LALT),                          KC_SLASH,         KC_4,           KC_5,           KC_6,           RCTL_T(KC_MINUS),
            KC_LALT,    KC_PC_CUT,     KC_BSLASH,      KC_PIPE,        KC_GRAVE,                               KC_PLUS,          KC_1,           KC_2,           KC_3,           KC_KP_DOT,
                                                           KC_NUMLOCK,     KC_TRAN,        KC_TRAN,       KC_TRAN, RSFT_T(KC_ENTER), KC_0
       ),
    [_MOUSE_F] = LAYOUT(

            KC_MS_WH_LEFT,  KC_MS_WH_DOWN,  KC_MS_UP,       KC_MS_WH_UP,    KC_MS_WH_RIGHT,                                 KC_F12,   KC_F1,  KC_F4,    KC_F4,          KC_PSCR,
            KC_MS_BTN1,     KC_MS_LEFT,     KC_MS_DOWN,     KC_MS_RIGHT,    KC_TRAN,                                        KC_F1,    KC_F4,          KC_F5,          KC_F9,          KC_F10,        
            KC_MS_BTN2,     KC_TRAN,        KC_TRAN,        KC_LGUI,        KC_TRAN,                                        KC_TRAN,  KC_F1,          KC_F2,        KC_F3,          KC_TRAN,
                                                            KC_TRAN,        KC_MS_BTN1,     KC_MS_BTN2,         KC_TRAN,    KC_TRAN, KC_TRAN
       ),
    [_SYMBOLS] = LAYOUT(
            KC_BSPACE,      KC_ESCAPE,      KC_ENTER,       KC_TRAN,        KC_TRAN,                                        KC_EQUAL,       KC_DQUO,        KC_QUOTE,       KC_BSLASH,      ST_MACRO_0,
            LSFT(KC_LALT),  KC_TRAN,        KC_TRAN,        TO(_GAME),      KC_TRAN,                                        KC_CIRC,        KC_ASTR,        KC_HASH,        KC_DLR,         KC_MINUS,
            KC_TRAN,        KC_TRAN,        KC_TRAN,        KC_TRAN,        KC_TRAN,                                        KC_PLUS,        KC_TILD,        KC_AT,          KC_DOT,         KC_UNDS,
                                                            KC_TRAN,        KC_TRAN, KC_TRAN,                      KC_TRAN, KC_TRAN,        KC_TRAN 
       ),
    [_GAME] = LAYOUT(
            KC_Q,     KC_W,   KC_E,           KC_R,         KC_T,                         KC_TRANSPARENT, KC_TRANSPARENT, KC_TRANSPARENT, KC_TRANSPARENT, KC_TRANSPARENT,
            KC_A,     KC_S,   KC_D,           KC_F,         KC_G,                         KC_TRANSPARENT, KC_TRANSPARENT, KC_TRANSPARENT, KC_TRANSPARENT, KC_TRANSPARENT,
            KC_Z,     KC_1,   KC_2,           KC_3,         KC_4,                         KC_TRANSPARENT, KC_TRANSPARENT, KC_TRANSPARENT, KC_TRANSPARENT, KC_TRANSPARENT,
                                                MO(_GAME_NUM),  KC_SPACE,   KC_ESCAPE,            KC_TRAN,  RSFT_T(KC_ENTER),  TO(_BASE) 
       ),
    [_GAME_NUM] = LAYOUT(
            KC_BSPACE,      KC_ESCAPE,     KC_ENTER,       KC_DQUO,    KC_TRAN,                                KC_EQUAL,         KC_7,           RSFT_T(KC_8),   KC_9,           KC_ASTR,
            KC_A,    KC_LGUI,       KC_LSHIFT,      KC_QUOTE,          LSFT(KC_LALT),                          KC_SLASH,         KC_4,           KC_5,           KC_6,           RCTL_T(KC_MINUS),
            KC_A,    KC_PC_CUT,     KC_BSLASH,      KC_PIPE,           KC_GRAVE,                               KC_PLUS,          KC_1,           KC_2,           KC_3,           KC_KP_DOT,
                                                           KC_NUMLOCK,     KC_TRAN,        KC_TRAN,       KC_TRAN, RSFT_T(KC_ENTER), KC_0
       ),

};

    /** [_NUMPAD] = LAYOUT( */
    /**         KC_TILD,        KC_EXLM,        KC_LBRACKET,    KC_RBRACKET,    LSFT(KC_TAB),                KC_HOME,        KC_PGDOWN,      KC_PGUP,        KC_DELETE,      LSFT(KC_F10), */
    /**         KC_LCTRL,       KC_TRANSPARENT, KC_LPRN,        KC_RPRN,        KC_TAB,                      KC_LEFT,        KC_DOWN,        KC_UP,          KC_RIGHT,       KC_RCTRL, */
    /**         KC_LALT,        KC_TRANSPARENT, KC_LCBR,        KC_RCBR,        KC_GRAVE,                    KC_END,         KC_BSPACE,      KC_WWW_BACK,    KC_WWW_FORWARD, KC_ENTER, */
    /**         KC_TRANSPARENT, KC_TRANSPARENT, KC_TRANSPARENT, KC_TRANSPARENT,  KC_TRANSPARENT, */
    /**         ), */

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    switch (keycode) {
        case ST_MACRO_0:
            if (record->event.pressed) {
                SEND_STRING(SS_LCTL(SS_TAP(X_R)) SS_DELAY(100) SS_LSFT(SS_TAP(X_QUOTE)));
            }
            break;
    }
    return true;
}

const uint16_t PROGMEM esc_combo[] = {KC_K, KC_J, COMBO_END};
combo_t key_combos[COMBO_COUNT] = {
    COMBO(esc_combo, KC_ESC)
};
