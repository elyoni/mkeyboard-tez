/* use <font/static/ShantellSans-ExtraBoldItalic.ttf> */
/* use <font/static/ShantellSans-BoldItalic.ttf> */
/* use <font/static/ShantellSans-ExtraBoldItalic.ttf> */
use <font/separate_statics/TTF/RecursiveMonoLnrSt-ExtraBold.ttf>
include <parameters.scad>
include <utils.scad>

height = total_thickness - backplate_case_flange;
/* text("TEZ2", font = "Shantell Sans ExtraBold"); */

/* translate([97,-26,height-plate_thickness*1/2]) */
/* use <font/static/ShantellSans-ExtraBoldItalic.ttf> */
/* translate([0,0,0]) */
/*     rotate(a=-45)linear_extrude(2) */
/*     text("TEZ2", size=10,font = "Shantell Sans:style=ExtraBold Italic"); */

/* text("T", size=10,font = "Shantell Sans:style=ExtraBold Italic"); */
text("E", size=10,font = "Recursive Mono Casual Static:style=ExtraBold");
#translate([0.9,1.7,0])
    text("E", size=8,font = "Recursive Mono Casual Static:style=ExtraBold");

/* #translate([0.6,0.4,0]) */
/*     resize([7.5,9.5,0], auto=true) */
/*     linear_extrude(3) */
/*     text("T", size=10,font = "Shantell Sans:style=ExtraBold Italic"); */
/* use <font/static/ShantellSans-BoldItalic.ttf> */
/* #translate([0,0,0]) */
/*     rotate(a=-45)linear_extrude(3) */
/*     text("TEZ2", size=9.5,font = "Shantell Sans:style=Bold Italic"); */

/* #translate([0.25,0.25,0]) */
/*     rotate(a=-45)linear_extrude(3) */
/*     text("TEZ2", size=9.5,font = "Shantell Sans ExtraBold"); */


/* translate([1,-25,0]) */
/*     linear_extrude(2) */
/*     text("YE", size=6, font = "Shantell Sans ExtraBold"); */
