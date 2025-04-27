
    window.addEventListener(
        'load', 
        function() {
            document.getElementById('loader-graphs-page').style.display = 'none' ;
            const content = document.getElementById('main-content-graphs-page');
            content.style.visibility = 'visible';
            content.style.position = 'static';  // Ripristina normale layout
        }
    );

