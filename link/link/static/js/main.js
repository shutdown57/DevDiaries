// function to set the height on fly
function autoHeight() {
$('#content').css('min-height', 0);
$('#content').css('min-height', (
    $(document).height() - $('#header').height() - $('#footer').height()
));
}

// onDocumentReady function bind
$(document).ready(function() {
    autoHeight();
});

// onResize bind of the function
$(window).resize(function() {
    autoHeight();
});
