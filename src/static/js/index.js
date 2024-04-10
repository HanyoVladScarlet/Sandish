// import '../js/constants'



let COLOR_INFO = '#70D470';
let COLOR_WARN = '#D4D470';
let COLOR_ERROR = '#D47070';


initialize();


let source = new EventSource('/api/stream');


// 后续的消息更新获取通过server推送的方式.
source.addEventListener('console_message', function(event) {
    let data = JSON.parse(event.data);
    console.log(data['message'])
    // TODO: 将回调函数独立出去.
    var color_hash = 'white';
    if (data['level'] == 1) {
        color_hash = COLOR_INFO
    }
    if (data['level'] == 2) {
        color_hash = COLOR_WARN
    }
    if (data['level'] == 3) {
        color_hash = COLOR_ERROR
    }
    html = `<span style="color:${color_hash}">${data['message']}</span><br/>`;
    $('#console').append(html);
});


// 监视属性变化
source.addEventListener('property_change', function(event){
    let data = JSON.parse(event.data);
})





function updateOutputImage() {
    $('img-front').attr('src', data['img_front_src']);
}


function displayMessage(res) {
    let items = []
    for (var i in res) {
        let item = res[i]
        var color_hash = 'white';
        if (res[i]['level'] == 1) {
            color_hash = COLOR_INFO
        }
        if (res[i]['level'] == 2) {
            color_hash = COLOR_WARN
        }
        if (res[i]['level'] == 3) {
            color_hash = COLOR_ERROR
        }
        text = `<span style="color:${color_hash}">${item['message']}</span><br/>`;
        items.push(text);
    }
    // console.log(res)
    let html = $('#console')
    // html.attr('readonly', false);
    // console.log(items.join(''));
    html.html(items.join(''));
    // html.attr('readonly', true);
};


/// <summary>
/// 向服务器发送启动渲染请求
/// </summary>
function beginRendering() {
    // console.log('Starting rendering process...')
    $.ajax({
        type: 'POST',
        url: '/api/start-rendering',
        dataType: 'json',
        data: {},
        success: function (res) {
            $('#b_render').prop("disabled", true);
            $('#e_render').prop("disabled", false);
            // console.log(res.data)
            // console.log('Rendering process started!');
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('错误：' + errorThrown);
        }
    });
};


/// <summary>
/// 向服务器发送停止渲染请求
/// </summary>
function endRendering() {
    // console.log('Interrupting rendering process...');
    $.ajax({
        type: 'GET',
        url: '/api/end-rendering',
        dataType: 'json',
        data: {},
        success: function (res) {
            $('#b_render').prop("disabled", false);
            $('#e_render').prop("disabled", true);
            // console.log(res.data)
            // console.log('Rendering process terminated!');
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('错误：' + errorThrown);
        }
    });
};


function getMessageQueue() {
    try {
        $.ajax({
            type: 'GET',
            url: '/api/get-message-queue',
            dataType: 'json',
            data: {},
            success: function (res) {
                displayMessage(res);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log('错误：' + errorThrown);
            }
        });
    }
    catch (e) {
        console.log('错误：' + e);
        // console.log('hao!');
        }
};



// 用于初始化组件
// 1. 获取当前服务器状态, 包括历史的console_log;
// 2. 初始化html组件状态, 比如一些按钮的enable_status等;
function initialize() {
    $('#b_render').prop("disabled", false);
    $('#e_render').prop("disabled", true);
    getMessageQueue();
}

// 弃用的轮询方法
// setInterval(function () {
//         getMessageQueue();
//     }, 1000);

