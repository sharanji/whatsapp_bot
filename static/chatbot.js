typing = `<div class="chat-bubble you" id="typing">
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto;display: block;shape-rendering: auto;width: 43px;height: 20px;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
    <circle cx="0" cy="44.1678" r="15" fill="#ffffff">
        <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.6s"></animate>
    </circle>
    <circle cx="45" cy="43.0965" r="15" fill="#ffffff">
        <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.39999999999999997s"></animate>
    </circle>
    <circle cx="90" cy="52.0442" r="15" fill="#ffffff">
        <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.19999999999999998s"></animate>
    </circle>
</svg>
</div>`;

var y = $('.chat-body').scrollTop(); //your current y position on the page
var chatHistory = localStorage.getItem("chats") ? JSON.parse(localStorage.getItem("chats")) : [];

$(document).ready(function() {
    $(".select2_el").select2({});
    chatHistory.forEach(msg => {
        if (msg['user'] != null) {
            $(".chat-body").append(`<div class="chat-bubble me">${msg['user']}</div>`)
        } else {
            $(".chat-body").append(`<div class="chat-bubble you">${msg['bot']}</div>`)
        }
    })
    $('.chat-body').scrollTop($('.chat-body').scrollTop() + $('.chat-body').height());

    $(".chat-bot-icon").click(function(e) {
        $(this).children('img').toggleClass('hide');
        $(this).children('svg').toggleClass('animate');
        $('.chat-screen').toggleClass('show-chat');
    });

    $('.end-chat').click(function() {
        $('.chat-body').addClass('hide');
        $('.chat-input').addClass('hide');
        $('.chat-session-end').removeClass('hide');
        $('.chat-header-option').addClass('hide');
    });

    $(".chat-bot-icon").click();

    $('#close_times').click(function() {
            $(".chat-bot-icon").click();
        })
        // $('#typing').hide();

});

$('.send_btn').click(function() {
    val = $('.input_box').val();
    if (val != "") {

        $('#typing').remove();
        $('.input_box').val('');
        $('.chat-body').append(`<div class="chat-bubble me">${val}</div>`);

        $('.chat-body').append(typing);
        $('.chat-body').scrollTop(y + 30000);

        $.ajax({
            url: window.location.href + '/ajax',
            type: 'get',
            data: {
                question: val,
            },
            success: function(response) {

                result = response.split("=");
                if (val != '') {
                    chatHistory.push({ "user": val });
                }
                if (Array.isArray(result)) {
                    result.forEach(e => {
                        chatHistory.push({ "bot": e });
                        $('.chat-body').append(`<div class="chat-bubble you">${e}</div>`);
                    });
                } else {

                    $('.chat-body').append(`<div class="chat-bubble you">${response}</div>`);
                }

                localStorage.setItem("chats", JSON.stringify(chatHistory));
                $('#typing').remove();

                y = $('.chat-body').scrollTop();
                $('.chat-body').scrollTop(y + 300);
            }
        });
    }
});