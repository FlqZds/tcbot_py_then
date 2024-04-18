//长按微信或者二维码

//定义一个函数，接受一个参数名作为参数
function getUrlParam(name) {
  //构造一个含有目标参数的正则表达式对象
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
  //匹配目标参数
  var r = window.location.search.substr(1).match(reg);
  //返回参数值，如果没有匹配到，则返回null
  if (r != null) return true;
  return false;
}

/**
 * 用户登录调用的js
 * @param  {[type]} url    [description]
 * @param  {[type]} LinkId [description]
 * @return {[type]}        [description]
 */
function login(){
    //初始化关键词
    window.keyword = '';
    window.from = '';
    var refer=document.referrer;
    $.ajax({
        url:'../server/get_keyword.php',
        data:{refer:refer},
        dataType:'JSON',
        type:'POST',
        async:false,
        success:function(data){
            console.log(data);
            window.keyword = data.keyword;
            window.from = data.from;
        },
        error:function(){

        },
    });
    //访问接口
    var params = { "id": window.link_id, "LinkName": "Index", "url": window.location.href,"keyword":window.keyword,"from":window.from,"refer":refer};
    var url = 'https://api.usbeststock.com/index.php/Home/Interface/pageView.html';
    $.ajax({
        url: url,
        type: "get",
        data: params,
        dataType: "text",
        success: function(data) {

            // if(data == '2'){
            //     window.location.href = "https://www.jlunecjusntldct.com"
            // }
        },
        error: function(data) {

        }
    });

}

function longPress(obj){
	obj.on({
		touchstart: function(e){
			timeOutEvent = setTimeout("presstj(0)",500);
		},
		touchmove: function(){
                clearTimeout(timeOutEvent);
                timeOutEvent = 0;
        },
		touchend: function(){
            clearTimeout(timeOutEvent);
            return false;
        }
	})
}

/**
 * 长按记录
 * @param  {[type]} LinkId [description]
 * @return {[type]}        [description]
 */
function presstj(LinkId){
    var code = !!window.gpCode ? window.gpCode : '';
    var phone = !!window.phone ? window.phone : '';
    var send_url = !!window.send_url ? window.send_url : '';
    var refer=document.referrer;
	var params = { "id": window.link_id, "LinkName": "Index", "url": window.location.href,"code":code,"keyword":window.keyword,"from":window.fm,"phone":phone,"server_id":window.server_id,"refer":refer};
    var url = 'https://api.usbeststock.com/index.php/Home/Interface/apply.html';
	$.ajax({
            url: url,
            type: "get",
            data: params,
            dataType: "text",
            success: function(data) {

            },
            error: function(data) {

            }
        });
    // if(window.link_id == 1223){
    //     window.link_id = 1117;
    // }
    // if(window.link_id == 1225){
    //     window.link_id = 1188;
    // }
    // params = { "id": window.link_id, "LinkName": "Index", "url": window.location.href,"code":code,"keyword":window.keyword,"from":window.fm,"phone":phone};
    // //如果号码不为空 且推送链接 则需要推送另一个
    if(phone != '' && send_url != ''){
        switch(window.link){
            case 'out1':
                params = {"LinkID":window.link_id,"Mobile":phone,"Reserve1":code,"From":window.fm};
                $.ajax({
                    url: send_url,
                    type: "get",
                    data: params,
                    dataType: "jsonp",
                    success: function(data) {

                    },
                    error: function(data) {

                    }
                });
                break;
            default:

                $.ajax({
                    url: send_url,
                    type: "get",
                    data: params,
                    dataType: "text",
                    success: function(data) {

                    },
                    error: function(data) {

                    }
                });
                break;
        }
    }
}

 function longPressByOCPC(obj,LinkId,convert_id){
	obj.on({
		touchstart: function(e){
			timeOutEvent = setTimeout("longPresstjByOCPC("+window.link_id+","+convert_id+")",500);
		},
		touchmove: function(){
                    clearTimeout(timeOutEvent);
                timeOutEvent = 0;
        },
		touchend: function(){
            clearTimeout(timeOutEvent);
            return false;
        }
	})
}

function longPresstjByOCPC(LinkId,convert_id){
	presstj(LinkId);
	_taq.push({convert_id:convert_id, event_type:"button"})
}

// function getWXInfo(wxNumObj,wxQRCodeUrlObj,wxNumObj2)
// {
// 	var params = { "id": window.link_id};
//     var url = 'http://47.101.11.172/jrdata/index.php/Home/Interface/getInfo.html?'+(new Date().getTime());
//     wxNumObj.text('扫一扫二维码'); //fanli8256
//     wxQRCodeUrlObj.attr("src",'../../images/lx836925.jpg');
// 	$.ajax({
//             url: url,
//             type: "get",
//             data: params,
//             dataType: "text",
//             async:false,
//             // jsonp: "callback",
//             // jsonpCallback: "JsonCallback",
//             success: function(data) {
//                 testjson = eval("(" + data + ")");
//                 if(testjson.ret==0 && testjson.data!=null){
//                     if(testjson.data.img == 'fanli8256.jpg'){
//                         wxNumObj.text('扫一扫二维码');//testjson.data.code
//                         wxQRCodeUrlObj.attr("src",'../../images/'+testjson.data.img);
//                         if(wxNumObj2){
//                             wxNumObj2.text(testjson.data.code);
//                         }
//                     }else{
//                         if(wxNumObj2){
//                             wxNumObj2.text(testjson.data.code);
//                         }
//                         setTimeout(function () {
//                             wxNumObj.text('扫一扫二维码');//testjson.data.code
//                             wxQRCodeUrlObj.attr("src",'../../images/'+testjson.data.img);
//                         }, 5000);
//                     }
// 				}else{
//                     if(wxNumObj2){
//                         wxNumObj2.text(testjson.data.code);
//                     }
//                     setTimeout(function () {
//                         wxNumObj.text('扫一扫二维码');//testjson.data.code
//                         wxQRCodeUrlObj.attr("src",'../../images/loading.png');
//                     }, 5000);
//                 }
//             },
//             error: function(data) {

//             }
//         });
// }


function getWXInfo(wxNumObj,wxQRCodeUrlObj,wxNumObj2)
{
    var params = { "id": window.link_id};
    var url = 'https://api.usbeststock.com/index.php/Home/Interface/getInfo.html?'+(new Date().getTime());
    wxNumObj.text('扫一扫二维码'); //fanli8256
    wxQRCodeUrlObj.attr("src",'../images/lx836925.jpg');
    $.ajax({
            url: url,
            type: "get",
            data: params,
            dataType: "text",
            async:false,
            // jsonp: "callback",
            // jsonpCallback: "JsonCallback",
            success: function(data) {
                testjson = eval("(" + data + ")");
                if(testjson.ret==0 && testjson.data!=null){
                    if(testjson.data.img == 'fanli8256.jpg'){
                        wxNumObj.text('扫一扫二维码');//testjson.data.code
                        wxQRCodeUrlObj.attr("src",'../images/'+testjson.data.img);
                        if(wxNumObj2){
                            wxNumObj2.text(testjson.data.code);
                        }
                    }else{
                        if(wxNumObj2){
                            wxNumObj2.text(testjson.data.code);
                        }
                        setTimeout(function () {
                            wxNumObj.text('扫一扫二维码');//testjson.data.code
                            wxQRCodeUrlObj.attr("src",'../images/'+testjson.data.img);
                        }, 5000);
                    }
                }else{
                    if(wxNumObj2){
                        wxNumObj2.text(testjson.data.code);
                    }
                    setTimeout(function () {
                        wxNumObj.text('扫一扫二维码');//testjson.data.code
                        wxQRCodeUrlObj.attr("src",'../images/loading.png');
                    }, 5000);
                }
            },
            error: function(data) {

            }
        });
}

function getWXInfo2(wxNumObj,wxQRCodeUrlObj)
{
    var params = { "id": window.link_id};
    var url = 'https://api.usbeststock.com/index.php/Home/Interface/getInfo.html?'+(new Date().getTime());
    $.ajax({
            url: url,
            type: "get",
            data: params,
            dataType: "text",
            async:false,
            // jsonp: "callback",
            // jsonpCallback: "JsonCallback",
            success: function(data) {
                testjson = eval("(" + data + ")");
                if(testjson.ret==0 && testjson.data!=null){
                    wxNumObj.text(testjson.data.code);//testjson.data.code
                    wxQRCodeUrlObj.attr("src",'../images/'+testjson.data.img);
                }else{
                    wxNumObj.text(testjson.data.code);//testjson.data.code
                    wxQRCodeUrlObj.attr("src",'../images/loading.png');
                }
            },
            error: function(data) {

            }
        });
}

function getQQInfo(wxNumObj,wxQRCodeUrlObj)
{
    var params = { "id": window.link_id};
    var url = 'https://api.usbeststock.com/index.php/Home/Interface/getInfo.html?'+(new Date().getTime());
    $.ajax({
            url: url,
            type: "get",
            data: params,
            dataType: "text",
            async:false,
            // jsonp: "callback",
            // jsonpCallback: "JsonCallback",
            success: function(data) {
                testjson = eval("(" + data + ")");
                if(testjson.ret==0 && testjson.data!=null){
                    wxNumObj.text(testjson.data.code);//testjson.data.code
                    wxQRCodeUrlObj.attr("src",'../images/'+testjson.data.img);
                    window.qq_url = testjson.data.url;
                }else{
                    wxNumObj.text(testjson.data.code);//testjson.data.code
                    wxQRCodeUrlObj.attr("src",'../images/loading.png');
                }
            },
            error: function(data) {

            }
        });
}


function getWSInfo()
{

    var params = { "id": window.link_id,"url":window.location.href,"refer":document.referrer};
    var return_url = {"url":'',"img":'','phone':''};
    var url = 'https://api.usbeststock.com/index.php/Home/Interface/getInfo.html?'+(new Date().getTime());
    $.ajax({
            url: url,
            type: "get",
            data: params,
            dataType: "text",
            async:false,
            // jsonp: "callback",
            // jsonpCallback: "JsonCallback",
            success: function(data) {
                testjson = eval("(" + data + ")");
                if(testjson.data!=null && testjson.data.url !='' ){
                    console.log(testjson.data.url);
                    return_url.url = testjson.data.url;
                    return_url.img = testjson.data.img;
                    return_url.phone = testjson.data.code;
                    return_url.ret = testjson.ret;

                    //返回需要点击的链接
                    //wxNumObj.text(testjson.data.code);//testjson.data.code
                //     wxQRCodeUrlObj.attr("src",'../images/'+testjson.data.img);
                //     window.qq_url = testjson.data.url;
                // }else{
                //     wxNumObj.text(testjson.data.code);//testjson.data.code
                //     wxQRCodeUrlObj.attr("src",'../images/loading.png');
                }
            },
            error: function(data) {

            }
        });
    return return_url;
}

/**
 *
 * @return {[type]} [description]
 */
function getLinkInfo(){
    var params = { "id": window.link_id};
    var url = 'https://api.usbeststock.com/index.php/Home/Interface/getLinkInfo.html?'+(new Date().getTime());
    $.ajax({
            url: url,
            type: "get",
            data: params,
            dataType: "json",
            async:false,
            success: function(data) {
                if(data.ret == 1){
                    switch(data.link){
                        case 'out1':
                            window.send_url = 'http://117.78.50.100:8080/stif/InputResource';
                            break;
                        default:
                            window.send_url = 'http://'+data.link+'/index.php/Home/Interface/accept';
                            break;
                    }
                    window.link = data.link;
                    window.fm = data.fm;
                    window.server_id = data.server_id;
                    console.log(window.send_url);
                    console.log(window.fm);
                }
            },
            error: function(data) {

            }
        });
}