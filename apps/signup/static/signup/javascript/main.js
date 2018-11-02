$(document).ready(function(){

    // add a new set in the create workout form
    $(document).on('click', '.add_set', function(){
        var url = '/add_set'

        var insert_position = $(this).prev()

        // this tells the form which exercise we're adding to
        $('#exercise_adding_to').attr('value', $(this).attr('id'))

        // data for ajax to send
        var data = $('#create-form').serialize();

        var updated_sets = parseInt($(this).prev().children('#exercise_' + $(this).attr('id') + '_sets').attr('value'))
        updated_sets ++;

        // this updates the number of sets in the exercise
        $(this).prev().children('#exercise_' + $(this).attr('id') + '_sets').attr('value', updated_sets)
        
        $.ajax({
            url : url,
            data : data,
            method : "POST"
        })
        .done(function(response){
            insert_position.append(response);
        })
    })
    

    // add a new exercise to the form
    $('.add_exercise').click(function(){
        var url = '/add_exercise'
        var data = $('#create-form').serialize()
        var insert_position = $(this)
        
        var num_exercises = parseInt($('#num_exercises').attr('value'))
        num_exercises ++
        $('#num_exercises').attr('value', num_exercises)
        
        $.ajax({
            url : url,
            data : data,
            method : "POST"
        })
        .done(function(response){
            insert_position.before(response)
        })
    })

    // listener for the record a workout page to populate the template with the details for a particular 
    // workout that a user has created
    $('.workout-select').click(function(){
        var data = $('#my-record-workout-form').serialize()
        var url = '/find_workout'
        var insert_position = $(this)

        $.ajax({
            url : url,
            data : data,
            method : "POST"
        })
        .done(function(response){
            $('#my_workout_details').html(response)
        })
    })

    //listener to delete a record
    $(document).on('click', '.delete', function(){
        var url = $(this).attr('id')
        var data = $(this).attr('id')
        $.ajax({
            url : url,
            data : data,
            method : 'GET'
        })
        .done(function(response){
            $('tbody').html(response)
        })
        return false;
    })




    // ajax signup form validation
    $('#first_name, #last_name, #email, #password, #confirm_password').keyup(function(){
        var data = $('#my-signup-form').serialize();
        var url = '/process_ajax';
        var listener = $(this);
        $.ajax({
            data : data, 
            url : url,
            method : "POST"
        })
        .done(function(response){
            listener.prev().html(response[listener.attr('id')])
            if (Object.keys(response).length > 0) {
                $('#my-signup-form').attr('onsubmit', 'return false');
            }

            else if (Object.keys(response).length == 0){
                $('#my-signup-form').attr('onsubmit', 'submit');
            }

            if (response[listener.attr('id')] == undefined){
                listener.prev().html('')
            }
            if (response['password'] == undefined){
                $('#password_p').html('')
            }

            else if (listener.attr('id') == 'confirm_password'){
                $('#password_p').html(response['password'])
            }
        })
    })

    // event listener to submit the create workout form
    $('#create_workout').click(function(){
        $('#create-form').submit();
    })


    $(document).on('click', '.update', function(){
        var url = '/update/' + $(this).attr('id')
        var data = $('.' + $(this).attr('id')).val()

        console.log(data)
        $.ajax({
            url : url,
            data : data,
            method : "GET"
        })
        .done(function(){

        })
    })

    // event listener to submit the log workout form
    $(document).on('click', '#submit-log-workout', function(){
        $('#my-record-workout-form').submit();
    })


    // event listener to submit the signup form
    $('#submit').click(function(){
        $('#my-signup-form').submit();
    })

    // event listener to submit the login form
    $('#submit').click(function(){
        $('#my-login-form').submit();
    })


})
