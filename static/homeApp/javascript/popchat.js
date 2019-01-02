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

function createChatMsg(msg, id){
    var date = formatAMPM(new Date());
    var avatar = me.avatar;
    var $li = $("<li>", {style: "100%"});
    var $msj_macro = $("<div>", {class: "msj macro"});
    var $avatar = $("<div>", {class: "avatar"}).html($("<img>", { class: "img-circle", style: "width:100%;", src: avatar}));
    var $textObj = $("<div>", {class: "text text-l"});
    var $msgObj = $("<p>", {text: msg});
    var $dateObj = $("<p>").append($("<small>", {text: date}));
    var $updateBut = $("<button>", {type: "button", text: "like!"}).click(upvoteFunction);
    var $hiddenId = $("<input>", {class: "msgId",id: "msgId", name: "msgId", type: "hidden", value: id, text: id});
    $li.append($msj_macro);
    $textObj.append($msgObj).append($dateObj);
    $msj_macro.append($avatar).append($textObj).append($hiddenId).append($updateBut);
    return $li;
}


//-- No use time. It is a javaScript effect.
function insertChat(who, text, id, time){
    if (time === undefined){
        time = 0;
    }
    console.debug("insertChat");
    console.debug("msg:" + text);
    console.debug("id:" + id);
    var $chatMsgObj = createChatMsg(text, id);
    setTimeout(
        function(){
            $("#specialUL").append($chatMsgObj);
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
    '/ws/chat/room/' + roomName + '/');

// var chatSocket = new WebSocket(
//     'ws://' + window.location.host +
//     '/ws/chat/' + 'personal token' + '/');

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    console.debug("onmessage" + data);
// {#        document.querySelector('#chat-log').value += (message + '\n');#}
    insertChat("me", data['popMessage']['msg'], data['popMessage']['id'], 0);
};

chatSocket.onclose = function(e) {
    console.log(e.reason);
    console.error('Chat socket closed unexpectedly:' + e.reason);
};

function upvoteFunction(){
    var id = $(this).parent().find('#msgId').val();
    chatSocket.send(JSON.stringify({
        'upvote': 'test',
        'id': id
    }));
}

function refreshFunction(){
    chatSocket.send(JSON.stringify({
        'refresh': 'test'
    }));
}

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
