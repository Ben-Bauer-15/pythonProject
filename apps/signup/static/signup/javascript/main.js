$(document).ready(function(){
    $('.add').click(function(){
        var url = '/add_set'
        var data = $('#my-signup-form').serialize()
        $.ajax({
            url : url,
            data : data,
            method : "POST"
        })
        .done(function(response){
            $('#insert-here').append(response);
            var set = $('#set').attr('value');
            set = parseInt(set) + 1;
            $('#set').attr('value', set);
        })

    })



    // $('.dropdown-toggle').mouseover(function(){
    //     $(this).next().addClass('show');
    // });
    // $('.dropdown-menu.show').mouseover(function(){
    //     $(this).css('display', 'block');
    // });

    
    // $('.dropdown-menu.show').mouseleave(function(){
    //     $(this).css('display', 'none');
    // });


});
