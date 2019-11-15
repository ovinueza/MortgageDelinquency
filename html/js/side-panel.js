/*-----------------------------------------------------------------------------------

    Theme Name: Canueza - Mortgage Modeling | Machine Learning | Data Analytics
    Description: One Page Portfolio Template
    Author: brianjlabelle.yahoo.com
    Version: 1.0

    /* ----------------------------------

    JS Active Code Index
            
        01. scrollIt for side panel
        
    ---------------------------------- */    

$(function() {

    "use strict";

    var wind = $(window);

    if (wind.width() > 992) {

        // scrollIt for side panel
        $.scrollIt({
          upKey: 38,                // key code to navigate to the next section
          downKey: 40,              // key code to navigate to the previous section
          easing: 'swing',          // the easing function for animation
          scrollTime: 600,          // how long (in ms) the animation takes
          activeClass: 'active',    // class given to the active nav element
          onPageChange: null,       // function(pageIndex) that is called when page is changed
          topOffset: 0            // offste (in px) for fixed top navigation
        });

    }
 
 
});
