
/* [Height] */

// Final height of the stack walls.
height = 50.0;

// ---------------------------------------------------------------------------------------------------------
// do not need to modify anything below here
// ---------------------------------------------------------------------------------------------------------
/* [Hidden] */

thickness = 2.0;
fudge = 0.1;

width = 38.5;
depth = 32.50;
 
cavity_width = width - thickness;
cavity_depth = depth - (2 * thickness);
cavity_height = height - (2 * thickness);

hole_diameter = 7.0;

slit_width = 4.0;
slit_height = 23.0;

// lid
rotate([0, 0, 180])
difference() {   
    union() {
        translate([30, 0, height / 2.0]) cube([2, depth, height], center = true);
        translate([28.5, 0, height / 2.0]) cube([1.5, cavity_depth, cavity_height], center = true);
    }
    translate([27, -6, 2]) cube([5, 12, 8]);
    
    translate([29, 0, 29]) rotate([0, 90, 0]) cube([1.5, 4, 5], center = true);
    translate([29, 0, 26]) rotate([0, 90, 0]) cube([1.5, 4, 5], center = true);

    translate([30, 8, 40]) rotate([0, 90, 0]) cylinder(h = 5, r1 = 2.1, r2 = 2.1, $fn=36, center = true);
    translate([28.5, 8, 40]) rotate([0, 0, 0]) cube([2, 6, 6], center = true);
    translate([30, 0, 40]) rotate([0, 90, 0]) cylinder(h = 5, r1 = 2.1, r2 = 2.1, $fn=36, center = true);
    translate([28.5, 0, 40]) rotate([0, 0, 0]) cube([2, 6, 6], center = true);
    translate([30, -8, 40]) rotate([0, 90, 0]) cylinder(h = 5, r1 = 2.1, r2 = 2.1, $fn=36, center = true);
    translate([28.5, -8, 40]) rotate([0, 0, 0]) cube([2, 6, 6], center = true);

    translate([26.5, 0, 27.5]) rotate([0, 90, 0]) cylinder(h = 5, r1 = 6, r2 = 6, $fn=36, center = true);

}


// base

//rotate([0, 0, 180])
union() {
    translate([13.5, -(cavity_depth / 2.0), 2]) cube([4.0, cavity_depth, 4.0]);
    translate([-16, -(cavity_depth / 2.0), 2]) cube([4.0, cavity_depth, 2.0]);    
    translate([-2, 12.5, 7]) cube([20.0, 2, 4.0]);    
    translate([-2, -14.5, 7]) cube([20.0, 2, 4.0]);    
    difference () {
        translate([0, 0, height / 2.0]) cube([width, depth, height], center = true); 
        translate([-1, 0, (cavity_height / 2.0) + thickness]) cube([cavity_width + fudge, cavity_depth, cavity_height], center = true);
        translate([-17.25, 13.0, 4]) cube([7, 5, 4]);         
        translate([22, 0, 72.5]) rotate([0, -45,0]) cube([width, depth + 2, 31], center = true);

        translate([18, 0, 15]) rotate([0, 90, 0]) cube([5.5,5.5,5.5], center = true);
        translate([18, 0, 35]) rotate([0, 90, 0]) cube([14, 25,3], center = true);

        translate([17.5, 4, 15]) rotate([0, 90, 0]) cube([2,2,2], center = true);
        translate([17.5, -4, 15]) rotate([0, 90, 0]) cube([2,2,2], center = true);
        
        translate([-18, 0, 29]) rotate([0, 90, 0]) cube([1.5, 4, 3], center = true);
        translate([-18, 0, 26]) rotate([0, 90, 0]) cube([1.5, 4, 3], center = true);
        
        translate([-18, 10, 40]) rotate([0, 90, 0]) cylinder(h = 3, r1 = 2.1, r2 = 2.1, $fn=36, center = true);
        translate([-18, 0, 40]) rotate([0, 90, 0]) cylinder(h = 3, r1 = 2.1, r2 = 2.1, $fn=36, center = true);
        translate([-18, -10, 40]) rotate([0, 90, 0]) cylinder(h = 3, r1 = 2.1, r2 = 2.1, $fn=36, center = true);
        
    }    
        
}

