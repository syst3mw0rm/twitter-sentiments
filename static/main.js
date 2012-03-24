$('document').ready(function() {
    updatestatus();
    scrollalert();
});

function updatestatus(){
    // Show the number of loaded items
    var totalItems = $('#tweets div').length;
    $('#status').text('Loaded '+totalItems+' Items');
}

function nearBottomOfPage() {
    return $(window).scrollTop() > $(document).height() - $(window).height() - 200;
}
  
function scrollalert(){

    if(nearBottomOfPage()) {
        //fetch new items
        $('#status').text('Loading more items...');
        // Ajax call
        // get the highest id of tweet
        var last_id = $('#tweets div').last().attr("id");
        $.get(last_id+'/append', function(data) {
            $('#tweets').append(data);
            console.log(data);
            updatestatus();
        });
        
    }

    setTimeout('scrollalert();', 1500);
}
