#include QMK_KEYBOARD_H
#include "features/layer_lock.h"

enum custom_keycodes {
  ST_MACRO_1,
  ST_MACRO_2,
  LLOCK,
};

/** enum layer_names { */
/**     BASE, */
/**     MDIA, */
/**     NUMB, */
/**     MOUS */
/** }; */
enum layer_names {
    BASE,
    MOVE,
    NUMPAD,
    MOUSE_F,
    SYMB,
    OTHER,
    GAMEM_L,
    GAMEM_R,
    GAME_NUM,

};

#ifdef RGBLIGHT_ENABLE
#define ERGOSLAB_BRIGHTNESS 200
#define HSV_ERGOSLAB_ORANGE 28, 255, 16
#define HSV_ERGOSLAB_RED 0, 255, ERGOSLAB_BRIGHTNESS
#define HSV_ERGOSLAB_GREEN 85, 255, ERGOSLAB_BRIGHTNESS
#define HSV_ERGOSLAB_CYAN 128, 255, ERGOSLAB_BRIGHTNESS
#define HSV_ERGOSLAB_TEST 100, 50, ERGOSLAB_BRIGHTNESS
#endif

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    // |--------------------|--------------------|--------------------|--------------------|--------------------|      |--------------------|--------------------|--------------------|--------------------|--------------------|
    [BASE] = LAYOUT_tez(
            KC_Q,                KC_W,                KC_E,                KC_R,                KC_T,                       KC_Y,                KC_U,                MT(MOD_RSFT, KC_I),  MT(MOD_RGUI, KC_O),  KC_P,
            MT(MOD_LCTL, KC_A),  MT(MOD_LGUI, KC_S),  MT(MOD_LSFT, KC_D),  LT(NUMPAD,KC_F),     KC_G,                       KC_H,                KC_J,                KC_K,                KC_L,                MT(MOD_RCTL, KC_SCOLON),
            MT(MOD_LALT, KC_Z),  KC_X,                KC_C,                LT(SYMB,KC_V),       KC_B,                       KC_N,                KC_M,                KC_COMMA,            KC_DOT,              LT(MOUSE_F,KC_SLASH),
            OSL(SYMB),           LT(NUMPAD,KC_SPACE), KC_LSHIFT,           MO(OTHER),                                                            KC_NO,               LT(SYMB,KC_BSPACE),  LT(MOVE,KC_ENTER),   KC_NO
            ),

    [MOVE] = LAYOUT_tez(
            KC_TRANSPARENT,      KC_EXLM,             KC_LBRACKET,         KC_RBRACKET,         LSFT(KC_TAB),               KC_HOME,             KC_PGDOWN,           KC_PGUP,             KC_DELETE,           LSFT(KC_F10),
            KC_LCTRL,            LSFT(KC_LALT),       KC_LPRN,             KC_RPRN,             KC_TAB,                     KC_LEFT,             KC_DOWN,             KC_UP,               KC_RIGHT,            KC_RCTRL,
            KC_LALT,             ST_MACRO_1,          KC_LCBR,             KC_RCBR,             KC_GRAVE,                   KC_END,              KC_INSERT,           KC_WBAK,             KC_WFWD,             KC_ENTER,
            KC_PRINT_SCREEN,     KC_TRANSPARENT,      KC_TRANSPARENT,      LLOCK,                                                                KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      TG(GAMEM_L)
            ),
    [NUMPAD] = LAYOUT_tez(
            KC_BSPACE,           KC_ESCAPE,           KC_ENTER,            KC_TRANSPARENT,      KC_GRAVE,                   KC_SLASH,            KC_7,                MT(MOD_RSFT, KC_8),  KC_9,                KC_ASTR,
            KC_LCTRL,            KC_LGUI,             KC_LSHIFT,           KC_TRANSPARENT,      KC_F,                       KC_EQUAL,            KC_4,                KC_5,                KC_6,                MT(MOD_RCTL, KC_MINUS),
            KC_LALT,             KC_CUT,              KC_COPY,             KC_PASTE,            KC_TRANSPARENT,             KC_PLUS,             KC_1,                KC_2,                KC_3,                KC_KP_DOT,
            KC_NUMLOCK,          KC_TRANSPARENT,      QK_BOOTLOADER,       LLOCK,                                                                QK_BOOTLOADER,       KC_TRANSPARENT,      KC_TRANSPARENT,      KC_0
            ),
    [MOUSE_F] = LAYOUT_tez(
            KC_MS_WH_LEFT,       KC_MS_WH_DOWN,       KC_MS_UP,            KC_MS_WH_UP,         KC_MS_WH_RIGHT,              KC_F11,             KC_F7,               KC_F8,               KC_F9,               KC_F12,        
            KC_MS_BTN1,          KC_MS_LEFT,          KC_MS_DOWN,          KC_MS_RIGHT,         RCTL(KC_RSHIFT),             KC_TRANSPARENT,     KC_F4,               KC_F5,               KC_F6,               KC_F10,        
            KC_MS_BTN2,          KC_MS_BTN3,          KC_COPY,             KC_PASTE,            LCTL(KC_LSHIFT),             KC_TRANSPARENT,     KC_F1,               KC_F2,               KC_F3,               KC_TRANSPARENT,
            KC_TRANSPARENT,      KC_MS_BTN1,          KC_MS_BTN2,          LLOCK,                                                                KC_TRANSPARENT,      KC_MS_BTN1,          KC_MS_BTN2,          KC_MS_BTN1 
            ),
        // |--------------------|--------------------|--------------------|--------------------|--------------------|      |--------------------|--------------------|--------------------|--------------------|--------------------|
        //
    [SYMB] = LAYOUT_tez(
            KC_CH_LNG,           KC_ESCAPE,           KC_ENTER,            KC_TRANSPARENT,      KC_TRANSPARENT,             KC_BSLASH,           RSFT(KC_BSLASH),     KC_QUOTE,            KC_DQUO,             ST_MACRO_2,    
            KC_M_ALL,            KC_TRANSPARENT,      KC_PASTE,            KC_TRANSPARENT,      KC_TRANSPARENT,             KC_CIRC,             KC_ASTR,             KC_HASH,             KC_DLR,              KC_UNDS,       
            KC_PC_UNDO,          KC_CUT,              KC_COPY,             KC_PASTE,            KC_TRANSPARENT,             KC_TRANSPARENT,      KC_TILD,             KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,
            KC_TRANSPARENT,      KC_TRANSPARENT,      KC_CH_LNG,           KC_TRANSPARENT,                                                       KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT
            ),
    [OTHER] = LAYOUT_tez(
            KC_VOLU,             KC_MUTE,             KC_BRIU,             RGB_M_B,             RGB_TOG,                    KC_NO,               KC_NO,               KC_NO,               KC_NO,               KC_NO,    
            KC_VOLD,             KC_NO,               KC_BRID,             KC_NO,               KC_NO,                      KC_NO,               KC_NO,               KC_NO,               KC_NO,               KC_NO,       
            KC_NO,               KC_NO,               KC_NO,               KC_NO,               QK_BOOTLOADER,              KC_NO,               KC_NO,               KC_NO,               KC_NO,               KC_NO,
            KC_NO,               KC_NO,               KC_NO,               KC_NO,                                                                KC_NO,               KC_NO,               KC_NO,               KC_NO 
            ),
    [GAMEM_L] = LAYOUT_tez(
            KC_Q,                KC_W,                KC_W,                KC_E,                KC_R,                       KC_ESCAPE,           KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,
            KC_LSHIFT,           KC_A,                KC_S,                KC_D,                KC_G,                       KC_LEFT,             KC_DOWN,             KC_UP,               KC_RIGHT,            KC_TRANSPARENT,
            KC_LCTRL,            KC_Z,                KC_X,                KC_C,                KC_V,                       KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,
            KC_B,                KC_SPACE,            OSL(GAMEM_R),        KC_ESCAPE,                                                            KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT
            ),
    /** [GAMEM_R] = LAYOUT_tez( */
    /**         KC_Y,                KC_U,                KC_I,                KC_O,                KC_P,                       KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT, */
    /**         KC_ESCAPE,           KC_J,                KC_K,                KC_L,                KC_SCOLON,                  KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT, */
    /**         TD(DANCE_0),         TD(DANCE_1),         TD(DANCE_2),         TD(DANCE_3),         TD(DANCE_4),                KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT, */
    /**         KC_TRANSPARENT,      KC_SPACE,            KC_TRANSPARENT,      KC_TRANSPARENT,                                                       KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT */
    /**         ), */
    /** [GAME_NUM] = LAYOUT_tez( */
    /**         TD(DANCE_5),        TD(DANCE_6),          TD(DANCE_7),         TD(DANCE_8),         TD(DANCE_9),                KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT, */
    /**         TD(DANCE_10),       TD(DANCE_11),         TD(DANCE_12),        TD(DANCE_13),        TD(DANCE_14),               KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT, */
    /**         TD(DANCE_15),       TD(DANCE_16),         TD(DANCE_17),        TD(DANCE_18),        TD(DANCE_19),               KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT, */
    /**         KC_TRANSPARENT,     KC_TRANSPARENT,       KC_TRANSPARENT,      KC_TRANSPARENT,                                                       KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT,      KC_TRANSPARENT */
    /**         ), */
};

bool process_record_user(uint16_t keycode, keyrecord_t *record) {

    if (!process_layer_lock(keycode, record, LLOCK)) { return false; }

    switch (keycode) {
        case ST_MACRO_1:
            if (record->event.pressed) {
                SEND_STRING(SS_LSFT(SS_TAP(X_SEMICOLON)) SS_DELAY(100) SS_TAP(X_Q) SS_DELAY(100) SS_LSFT(SS_TAP(X_1)));
            }
            break;
    }

    return true;
}

#ifdef RGBLIGHT_ENABLE
layer_state_t layer_state_set_user(layer_state_t state) {
  uint8_t layer = get_highest_layer(state);
  switch (layer) {
      case BASE:
          rgblight_sethsv(HSV_ERGOSLAB_ORANGE);
        break;
      case MOVE:
          rgblight_sethsv(HSV_ERGOSLAB_RED);
        break;
      case NUMPAD:
          rgblight_sethsv(HSV_ERGOSLAB_GREEN);
        break;
      case MOUSE_F:
          rgblight_sethsv(HSV_ERGOSLAB_CYAN);
        break;
      case GAMEM_L:
      case GAMEM_R:
          rgblight_sethsv(HSV_ERGOSLAB_TEST);
        break;
      default:
        break;
    }
  return state;
};
#endif
