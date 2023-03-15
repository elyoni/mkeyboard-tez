include <parameters.scad>
include <utils.scad>

socket_border = 2;


module typec(borders=[0,0,0,0]) {
    /* translate([h_unit/2,-socket_length,0]) */
    /*     rotate([0,layout_type == "row"?180:0,0]) */
    /*         translate([-socket_width/2,0,-pcb_thickness/2]) */
    /* typec_connector(invert_borders(borders,layout_type == "row")); */
    socket_length = typec_inner_length+typec_middle_length+typec_outer_length + socket_border;
    socket_height = max(typec_inner_height,typec_middle_height,typec_outer_height);
    socket_width = max(typec_inner_width,typec_middle_width,typec_outer_width) + socket_border;
    #difference() {
        cube([typec_inner_length+typec_middle_length+typec_outer_length,
               socket_width,
               socket_height], center=true);
        typec_connector(invert_borders(borders,layout_type == "row"));
    }

    translate([0,0,-(socket_height+pcb_thickness/2)/2])

        cube([socket_length + socket_border,
              socket_width + socket_border,
              pcb_thickness/2], center=true);
    
}

module typec_connector(borders=[0,0,0,0]){
    full_length = typec_outer_length+typec_middle_length+typec_inner_length;
    /* translate([-typec_outer_length+(+typec_middle_length+typec_inner_length)/2,0,0]) */
    translate([-full_length/2+typec_outer_length/2,0,0])
    union() {
        cube([typec_outer_length,
              typec_outer_width,
              typec_outer_height], center=true, anchor=CENTER);

        translate([(typec_outer_length+typec_middle_length)/2,
                   0,
                   0])
            cube([typec_middle_length,
                  typec_middle_width,
                  typec_middle_height], center=true);
        translate([(typec_outer_length+typec_inner_length)/2+typec_middle_length,
                   0,
                   0])
            cube([typec_inner_length,
                  typec_inner_width,
                  typec_inner_height], center=true);
    }

    /* union() { */
    /*     cube([typec_outer_length, */
    /*           typec_outer_width, */
    /*           typec_outer_height]); */
    /*  */
    /*     translate([(typec_outer_length+typec_middle_length)/2, */
    /*                -(typec_middle_width-typec_outer_width)/2, */
    /*                0]) */
    /*         cube([typec_middle_length, */
    /*               typec_middle_width, */
    /*               typec_middle_height]); */
    /*     translate([full_length/2, */
    /*                0, */
    /*                0]) */
    /*         cube([typec_inner_length, */
    /*               typec_inner_width, */
    /*               typec_inner_height], center=true); */
    /* } */
    /* translate([(typec_outer_length/2+typec_middle_length/2+typec_inner_length/2)/2, */
    /*            0, */
    /*            0]) */
    /* #cube([typec_inner_length+typec_middle_length+typec_outer_length, */
    /*        max(typec_inner_width,typec_middle_width,typec_outer_width), */
    /*        max(typec_inner_height,typec_middle_height,typec_outer_height)], center=true); */
    /* cube([socket_width,socket_length,pcb_thickness-2+trrs_flange_diameter*2/3]); */


}


typec();
