var me = {};
me.avatar = "https://lh6.googleusercontent.com/-lr2nyjhhjXw/AAAAAAAAAAI/AAAAAAAARmE/MdtfUmC0M4s/photo.jpg?sz=48";

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}

function upvoteFunction(who){
    // console.log(Object.getOwnPropertyNames(who));
}

//-- No use time. It is a javaScript effect.
function insertChat(who, text, time){
    if (time === undefined){
        time = 0;
    }
    console.debug("insertChat");
    console.debug(text.msg);
    var control = "";
    var date = formatAMPM(new Date());
    var avatar = me.avatar;
    control = '<li style="width:100%">' +
            '<div class="msj macro">' +
            '<div class="avatar"><img class="img-circle" style="width:100%;" src="' + avatar + '" /></div>' +
                '<div class="text text-l">' +
                    '<p>' + text.msg + '</p>' +
                    '<p><small>' + date + '</small></p>' +
                '</div>' +
                '<button type="button" onclick=upvoteFunction();>Upvote!</button>' +
            '</div>' +
        '</li>';
    setTimeout(
        function(){
            $("#specialUL").append(control).scrollTop($("#specialUL").prop('scrollHeight'));
        }, time);

}

function resetChat(){
    $("#specialUL").empty();
}



// {#    $('#chat-message-submit > span').click(function(){#}
// {#        $   (".mytext").trigger({type: 'keydown', which: 13, keyCode: 13});#}
// {#    })#}

//-- Clear Chat
resetChat();



// var roomName = {{ room_name_json }};
/*
var roomName = "";
function setRoomName(room){
    roomName = room;
}
*/

var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/chat/' + roomName + '/');

chatSocket.onmessage = function(e) {


    var data = JSON.parse(e.data);
    console.debug("onmessage" + data['popMessage'].toString());
    var message = data['popMessage']['msg'];
// {#        document.querySelector('#chat-log').value += (message + '\n');#}
    insertChat("me", message, 0);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('.mytext').focus();
document.querySelector('.mytext').onkeyup = function(e) {
    console.debug("onkeyup");
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};
$(".mytext").on("keydown", function(e){
    console.debug("onkeydown");
    if (e.which == 13){
        var messageInputDom = document.querySelector('.mytext');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
//            print("test:"+message);#}
        messageInputDom.value = '';
    }
});
