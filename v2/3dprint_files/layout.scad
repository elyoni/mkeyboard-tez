include <parameters.scad>
include <stabilizer_spacing.scad>

/* [Layout Values] */
/* Layout Format (each key):
    [
        [                                       // Location Data
            [x_location, y_location],
            key_size,
            [rotation, rotation_x, rotation_y],
        ],
        [                                       // Borders
            top_border,
            bottom_border,
            left_border,
            right_border
        ],
        extra_data                              // Extra data (depending on component type)
    ]
*/

// Keyswitch Layout
//     (extra_data = rotate_column)
base_switch_layout = [
  [[[2,0],1,[0,0,0]],[0,1,1,1],false],
  [[[1,0.13],1,[0,0,0]],[0,1,1,1],false],
  [[[3,0.13],1,[0,0,0]],[0,1,1,1],false],
  [[[4,0.25],1,[0,0,0]],[0,1,1,1],false],
  [[[0,0.38],1,[0,0,0]],[0,1,0,1],false],
  [[[2,1],1,[0,0,0]],[1,1,1,1],false],
  [[[1,1.13],1,[0,0,0]],[1,1,1,1],false],
  [[[3,1.13],1,[0,0,0]],[1,1,1,1],false],
  [[[4,1.25],1,[0,0,0]],[1,1,1,1],false],
  [[[0,1.38],1,[0,0,0]],[1,1,0,1],false],
  [[[2,2],1,[0,0,0]],[1,4,1,1],false],
  [[[1,2.13],1,[0,0,0]],[1,3,1,1],false],
  [[[3,2.13],1,[0,0,0]],[1,3,1,1],false],
  [[[4,2.25],1,[0,0,0]],[1,2,1,1],false],
  [[[0,2.38],1,[0,0,0]],[1,1,0,1],false],
  //[[[5,2.75],1,[0,0,0]],[1,2,2,1],false],
  [[[5,3.6],1,[-30,6.5,4.25]],[3.5,1,3,1],false],
  [[[4,4.6],1,[-30,6.5,4.25]],[3.5,0,3,1],false],
  [[[5,4.6],1,[-30,6.5,4.25]],[4.2,0,1,1],false],
  [[[6,4.6],1,[-30,6.5,4.25]],[1  ,0,1,0],false],
];


// MCU Position(s)
base_mcu_layout = [
    [[[5.1,0.51],1.5,[0,0,0]],[0,42.5,3,1],false],
	//[[[-4.5,1.6],1.5,[90,0,0]],[14,6,0,0],false]
];

// TRRS Position(s)
base_trrs_layout = [ 	              
   /* //[[[5,0.5],1,[0,0,0]],[0,0,0,0]], */
   [[[6.4,3.35],1,[-90,7,3]],[0,0,0,0]],
];

base_typec_layout = [ 	              
   //[[[5,0.5],1,[0,0,0]],[0,0,0,0]],
   [[[6.4,3.35],1,[-90,7,3]],[0,0,0,0]],
];

// Stabilizer layout
//     (extra_data = [key_size, left_offset, right_offset, switch_offset=0])
//     (see stabilizer_spacing.scad for presets)
base_stab_layout = [];

// Via layout
//     (extra_data = [via_width, via_length])
base_via_layout = [
    [[[4.55, 1.95]]],
    [[[4.55, 0.95]]],
    [[[4.55, 0.0]]],

    [[[4.8, 2.6]]],
];

// Plate Layout (if different than PCB)
//     (extra_data = component_type)
base_plate_layout = [];

// Whether to only use base_plate_layout to generate the plate footprint
use_plate_layout_only = false;

// Standoff layout
//     (extra_data = [standoff_integration_override, standoff_attachment_override])
base_standoff_layout = [
    [[[0.5,0.125]]], // original
    [[[0.5,2.2]]], // original
    [[[2.5,1]]], // original
    [[[4.5,0.5]]], // original
    [[[5.8,3.7]]], // original

    /* [[[0.5, 0.2]]], // new */
    /* [[[2.5, 0.0]]], // new -- */
    /* [[[4.5, 0.2]]], // new */

    /* [[[0.5, 1.3]]], // new -- */
    /* [[[2.5,1.0]]], // new -- */
    /* [[[4.5,1.3]]], // new -- */

    /* [[[0.5, 2.6]]], // new */
    /* [[[2.5,2.4]]], // new -- */
    /* [[[4.5,2.7]]], // new -- */

    /* [[[5.4, 3.8]]], // new */
    /* [[[4.0, 4.2]]], // new -- */

    // PCB-Backplate standoffs
    /* [[[-0.5,-0.375]],[0,0,0,0],["plate", "backplate"]], */
    /* [[[-0.5,0]],[0,0,0,0],["plate", "backplate"]], */
    [[[-0.5,0]],[0,0,0,0],["plate", "backplate"]],
    [[[-0.5,3]],[0,0,0,0],["plate", "backplate"]],
    [[[6.2,-0.04]],[0,0,0,0],["plate", "backplate"]],
    [[[6.2,3.5]],[0,0,0,0],["plate", "backplate"]],
    [[[3,4.1]],[0,0,0,0],["plate", "backplate"]],
    /* [[[-0.5,3.625]],[0,0,0,0],["plate", "backplate"]], */
    /* [[[4,3.625]],[0,0,0,0],["plate", "backplate"]], */
    /* [[[4.125,6.125],1.5,[60,4.875,4.625]],[0,0,0,0],["plate", "backplate"]], */
    /* [[[6.5,3]],[0,0,0,0],["plate", "backplate"]], */
    /* [[[5.5,-0.1875]],[0,0,0,0],["plate", "backplate"]], */
    /* [[[7,0]],[0,0,0,0],["plate", "backplate"]], */
];

// Whether to flip the layout
invert_layout_flag = true;

// Whether the layout is staggered-row or staggered-column
layout_type = "column";  // [column, row]
