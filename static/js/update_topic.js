function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    $('.update_topic').on('click', function (e) {
        e.preventDefault();
        let board_pk = $(this).attr('board-pk');
        let topic_pk = $(this).attr('topic-pk');
        let token = $(this).attr('token');
        $.ajax({
            url: `topics/${topic_pk}/update/`,
            type: 'post',
            dataType: 'json',
            data: {
                'board_pk': board_pk,
                'topic_pk': topic_pk,
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            beforeSend: function () {
                $("#modal-topic").modal("show");
            },
            success: function (data) {
                $("#modal-topic .modal-content").html(data.html_form);
            }
        });
    });
    $('.delete_topic').on('click', function (e) {
        e.preventDefault();
        let board_pk = $(this).attr('board-pk');
        let topic_pk = $(this).attr('topic-pk');
        $.ajax({
            url: `topics/${topic_pk}/delete/`,
            type: 'post',
            dataType: 'json',
            data: {
                'board_pk': board_pk,
                'topic_pk': topic_pk,
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            beforeSend: function () {
                $("#modal-topic").modal("show");
                console.log('QQ');
            },
            success: function (data) {
                $("#modal-topic .modal-content").html(data.html_form);
                console.log(data)
            }
        });
    });
});