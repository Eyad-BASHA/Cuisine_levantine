$(document).ready(function () {
    
    // $('input[type="file"]').attr("multiple", "true");
    $('input[type="file"]').attr("id", "fileupload");
    $('input[type="file"]').attr("accept", "image/*, video/*");
    
    // $('input[name="birth_date"]').addClass("datepicker");
    $('input[name="birth_date"]').attr("placeholder", "Selected date");
    // $('input[name="birth_date"]').attr("data-provide", "datepicker");

    $('#reply-form').find('textarea').attr("placeholder", "Votre Répondre");

    // $('#like').on('click', function(event){
    //     event.preventDefault();
    //     var pk = $(this).attr('value');
    //     $.ajax({
    //         type: 'POST', 
    //         url: '{% url "like_article" %}', 
    //         data: {'article_id': pk, 'csrfmiddlewaretoken': '{{ csrf_token }}' }, 
    //         dataType: 'json', 
    //         success: function(response){
    //             $('.like-section').html(response['form'])
    //             console.log($('.like-section').html(response['form']));
    //         },
    //         error: function(rs, e){
    //             console.log(rs.responseText); 
    //         },
    //     });
    // })

    // $('#id_birth_date').datetimepicker({
    //     timepicker: false,
    //     datepicker: true,
    //     format: 'Y-m-d',
    //     weeks: true,

    // });

    // $(function () {
    //     $("#datetimepicker1").datetimepicker();
    // });

    // accept="image/*,.pdf">

    // $(".add-multiple").each(function(i) {
    //   $(this).find('input').attr('name', 'media[]');
    // });

    $('.add-multiple').each(function(i) {
        $(this).find('input[type="file"]').attr("multiple", "true");
        // $(this).append('<img src="" alt="" class="rounded-circle account-img mr-3" width="50px">');
    });

    $('#div_id_profile_pic').each(function(i) {
        $(this).find('a').attr("target","_blank");
        // $(this).append('<img src="" alt="" class="rounded-circle account-img mr-3" width="50px">');
    });
    

    $(".alert").delay(6000).slideUp(1000, function () {
        $(this).alert('close');
    });

    // $('btn-alert-message').click(function(){
    $('#comment-alert').click(function(){
        $('#alert-message-comment').html("vous devez connecter ou vous êtes bloqué");
        $("div.alert-danger").removeClass("d-none");
    });

    $('.reply-btn').click(function(){
        $(this).parent().parent().next().next('.replied-comments').removeClass("d-none");
    });


    $('#btn-add-article').click(function(){
        $("div#add-article").toggleClass("d-none");
    });

    $('.dateinput').attr('type', 'date');

    $('#btn-filter').click(function(){
        $("div#filter").toggleClass("d-none");
    });

    // ==== Changer la label de la fimter ======== 
    $('div#filter').find('label[for="id_language"]').html('Langue');
    $('div#filter').find('label[for="id_auther"]').html('Auteur');
    $('div#filter').find('label[for="id_category"]').html('Catégorie');
    $('div#filter').find('label[for="id_sub_category"]').html('Sous Catégorie');
    $('div#filter').find('label[for="id_title"]').html('Titre');



    // comment with ajax 
    // $(document).on('submit', '.comment-form', function(event){
    //     event.preventDefault();
    //     $.ajax({
    //         type: "POST",
    //         url: $(this).attr('action'),
    //         data: $(this).serialize(),
    //         dataType: 'json',
    //         success: function (response){
    //             $('.main-comments').html(response['form']);
    //             $('textarea').val('');
                // $('.reply-btn').click(function(){
                //     $(this).parent().parent().next().next('.replied-comments').removeClass("d-none");
                        // $('textarea').val('');
                // });
    //         },
    //         error: function (rs, e){
    //             console.log(rs.responseText);
    //         },
    //     });
    // });

    // $(function () {
    //     $("#mdb-lightbox-ui").load("mdb-addons/mdb-lightbox-ui.html");
    // });

    // $(function () {
    //     $("#mdb-lightbox-ui").load("{% static 'mdb-addons/mdb-lightbox-ui.html' %}");
    // });

    // MDB Lightbox Init
    // $(function () {
    //     $("#mdb-lightbox-ui").load("mdb-addons/mdb-lightbox-ui.html");
    // });

    // MDB Lightbox Init
   
    


    // $('.carousel-3d-basic').mdbCarousel3d();

    // $('#myCarousel').on('slide.bs.carousel', function () {
    //     // do something…
    // })

    // $('.carousel').carousel({
    //     interval: 500
    // })



    // $(function($) {
    //   $('#create-article').submit(function (event){
    //       var data = new FormData(this);
    //       var action = function (d) {
    //         console.log(d)
    //       }; 

    //       $.ajax({ 
    //         url: 'home', 
    //         type: 'POST', 
    //         data: data,
    //         contentType: false, 
    //         processData: false, 
    //         success: action, 
    //         error: action  
    //       });
    //   });
    // }(jQuery));

    // $(function () {
    //     /* 1. OPEN THE FILE EXPLORER WINDOW */
    //     // $(".js-upload-photos").click(function () {
    //     //   $("#fileupload").click();
    //     // });

    //     /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
    //     $("#fileupload").fileupload({
    //       dataType: 'json',
    //       done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
    //         if (data.result.is_valid) {
    //           $("#gallery tbody").prepend(
    //             "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
    //           )
    //         }
    //       }
    //     });

    //   });




});


