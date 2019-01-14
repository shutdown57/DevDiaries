$('button.delete').on('click', function (evt) {
    $('article.message.is-danger').remove();
    evt.preventDefault();
});
