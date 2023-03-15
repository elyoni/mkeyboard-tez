#include QMK_KEYBOARD_H

enum layer_names {
    BASE,
    MDIA,
    NUMB,
    MOUS
};

#ifdef RGBLIGHT_ENABLE
#define ERGOSLAB_BRIGHTNESS 112
#define HSV_ERGOSLAB_ORANGE 28, 255, 16
#define HSV_ERGOSLAB_RED 0, 255, ERGOSLAB_BRIGHTNESS
#define HSV_ERGOSLAB_GREEN 85, 255, ERGOSLAB_BRIGHTNESS
#define HSV_ERGOSLAB_CYAN 128, 255, ERGOSLAB_BRIGHTNESS
#endif

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
  [BASE] = LAYOUT_ergoslab(
    KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,
    KC_A,    KC_S,    KC_D,    KC_F,    KC_G,
    KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,
    KC_Q,    KC_Q,    KC_Q,    QK_BOOT 
  ),
};

#ifdef RGBLIGHT_ENABLE
/** layer_state_t layer_state_set_user(layer_state_t state) { */
/**   uint8_t layer = get_highest_layer(state); */
/**   switch (layer) { */
/**       case BASE: */
/**           rgblight_sethsv(HSV_ERGOSLAB_ORANGE); */
/**         break; */
/**       case MDIA: */
/**           rgblight_sethsv(HSV_ERGOSLAB_RED); */
/**         break; */
/**       case NUMB: */
/**           rgblight_sethsv(HSV_ERGOSLAB_GREEN); */
/**         break; */
/**       case MOUS: */
/**           rgblight_sethsv(HSV_ERGOSLAB_CYAN); */
/**         break; */
/**       default: */
/**         break; */
/**     } */
/**   return state; */
/** }; */
#endif
