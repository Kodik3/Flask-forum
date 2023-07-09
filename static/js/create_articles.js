import Request from './Request.js';


$(document).ready(function() {
    $('.content-button').click(function(event) {
        event.preventDefault();

        let content = $('.content').val();
        let data = { content: content };

        Request.post('/api/v1/create_articles_app', data)
            .then(function(response) {
                if (response === 1) {
                    $('#error').html('Article cannot be more than 1000 characters!');
                } else if (response === 2) {
                    $('#error').html('Article cannot be less than one character!');
                } else {
                    window.location.href = '/main';
                }
            })
    });
});