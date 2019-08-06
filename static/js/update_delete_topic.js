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


$('.update_topic').on('click', function (e) {
    let board_pk = $(this).attr('board-pk');
    let topic_pk = $(this).attr('topic-pk');
    var form = $(this);
    e.preventDefault();
    $.ajax({
        url: `topics/${topic_pk}/update/`,
        type: 'post',
        dataType: 'json',
        data: {
            'board_pk': board_pk,
            'topic_pk': topic_pk,
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        beforeSend: function (data) {
            $("#modal-topic-update").modal("show");
        },
        success: function (data) {
            $("#modal-topic-update .modal-content").html(data.html_form);
        }
    });
    return false;
});

$("#modal-topic-update").on("submit", ".js-topic-update-form", function () {
    var form = $(this);
    console.log(form);
    let subject = document.getElementById("id_subject").value;

    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                $("#modal-topic-update").modal("hide");
                // $(`#${data.board_pk}-${data.topic_pk}`).hide();
                $(`#${data.board_pk}-${data.topic_pk}-subject`).html(subject);
                $(`#${data.board_pk}-${data.topic_pk}-last-update`).html(data.naturaldelta);
            } else {
                $("#modal-topic-update .modal-content").html(data.html_form);
            }
        }
    });
    return false;
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
            $("#modal-topic-delete").modal("show");
        },
        success: function (data) {
            $("#modal-topic-delete .modal-content").html(data.html_form);
        }
    });
});

$("#modal-topic-delete").on("submit", ".js-topic-delete-form", function () {
    var form = $(this);
    console.log(form);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            if (data.confirmed) {
                $("#modal-topic-delete").modal("hide");
                $(`#${data.board_pk}-${data.topic_pk}`).hide();
            } else {
                $("#modal-topic-delete .modal-content").html(data.html_form);
            }
        }
    });
    return false;
});
