// var bindings = {};
// Manifest
//
// var manifest = {
//
  // Bindings
//
  // ui: {
//
    // "#url-create": { bind: "url-create" },
//
    // "#img-create" : { bind: "img-create" }
//
  // },
//
// };
//
// Init $.my over DOM node
//
// $("#link-create").my( manifest, bindings );
//
// var get_and_set_image = function (resp) {
    // var get_data = {
        // img_url: resp.image_url,
        // img_name: $('#name-create').val()
    // };
    // var rsp = {};
//
    // $.ajax({
        // url: $SCRIPT_ROOT + '/links/get-website-image',
        // method: 'POST',
        // headers: {
            // 'Content-Type': 'application/json'
        // },
        // data: JSON.stringify(get_data)
    // }).done(function (response) {
        // console.log(response);
        // rsp = response;
            // clearInterval(intervalID);
            // $("input").prop('disabled', false);
            // $("#make-web-img-create").removeClass("is-loading");
            // $("#img-create").val(resp.image_url);
        // setTimeout(function () {
        // }, 9000);
    // }).fail(function (rej) {
        // console.error(rej);
    // });
    // return rsp;
// };
//
// $('#make-web-img-create').on('click', function (evt) {
    // var make_data = {
        // img_url: $('#url-create').val(),
        // img_name: $('#name-create').val()
    // };
    // $.ajax({
        // url: $SCRIPT_ROOT + '/links/make-website-image',
        // method: 'POST',
        // headers: {
            // 'Content-Type': 'application/json'
        // },
        // data: JSON.stringify(make_data)
    // }).done(function (resp) {
        // $("input").prop('disabled', true);
        // $("#make-web-img-create").addClass("is-loading");
        // var intervalID = setInterval(function () {
            // get_and_set_image(resp);
        // }, 3000, resp);
    // }).fail(function (rej) {
        // console.error(rej);
    // });
//
    // evt.preventDefault();
// });

$('#form-create-submit').on('click', function (evt) {
    $('#').submit(function (evt) {
        var form_create = $(this);
        var send_url = form_create.attr('action');
        $("input").prop('disabled', true);
        $("#make-web-img-create").addClass("is-loading");
        $.ajax({
            url: $SCRIPT_ROOT + '/links/store',
            method: 'POST',
            data: form_create.serialized(),
        }).done(function (resp) {
            console.log(resp);
            $("input").prop('disabled', false);
            $("#make-web-img-create").removeClass("is-loading");
        }).fail(function (rej) {
            console.error(rej);
        });
    });

    evt.preventDefault();
});
