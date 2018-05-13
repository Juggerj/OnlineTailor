/**
 * Created with PyCharm.
 * User: Jugger
 * Date: 22.03.17
 * Time: 21:50
 * To change this template use File | Settings | File Templates.
 */
"use strict"

window.onresize = function(){
    change_size("questions");
    change_size("program");
    change_size_float('offer-float');
    change_size('offer');
}

function quest(item){
    item.childNodes[3].style.display = item.childNodes[3].style.display == "block" ? "none" : "block";
    change_size("questions");
}

function them(item){
    for (var i = 2; i<item.childNodes.length;i++){

        if (item.childNodes[i].nodeName == 'P'){
//            console.log(item.childNodes[i].nodeName);
            item.childNodes[i].style.display = item.childNodes[i].style.display == "block" ? "none" : "block";
        }

    }

    change_size("program");
}

function change_size(main){
    var el = document.getElementById(main)
    var res = 0;
//    console.log(main);
//    console.log(el);

    try{
        for (var i=0; i< el.children.length; i++){
            res += Number(getComputedStyle(el.children[i]).height.replace('px',''))
                +  Number(getComputedStyle(el.children[i]).marginTop.replace('px',''))
                +  Number(getComputedStyle(el.children[i]).marginBottom.replace('px',''))
                +  Number(getComputedStyle(el.children[i]).paddingTop.replace('px',''));
    //        console.log(res);
    //        console.log(el.children[i]);

        }
        el.style.height = (res) + 'px';
    } catch (e){}
    return null;
}

function change_size_float(main){
    var el = document.getElementById(main);
    var res = 0;

    for (var i=0; i< el.children.length; i++){
        if (Number(getComputedStyle(el.children[i]).height.replace('px',''))
            +  Number(getComputedStyle(el.children[i]).marginTop.replace('px',''))
            +  Number(getComputedStyle(el.children[i]).marginBottom.replace('px',''))
            +  Number(getComputedStyle(el.children[i]).paddingTop.replace('px','')) > res)
        {

            res = Number(getComputedStyle(el.children[i]).height.replace('px',''))
            +  Number(getComputedStyle(el.children[i]).marginTop.replace('px',''))
            +  Number(getComputedStyle(el.children[i]).marginBottom.replace('px',''))
            +  Number(getComputedStyle(el.children[i]).paddingTop.replace('px',''));
        }
//        console.log(res);
    }
    el.style.height = (res) + 'px';
}

function change_recall_base(dir,cur){
    $.ajax({
        url: 'recall/' + dir + '/' + cur,
        type: 'GET',
        dataType: 'json',
        success: function (response){
            if (response.errors) {
                console.log("errors = ", errors);
            } else {
                $('.all').html(response.html);
            }
        },
        error: function (xhr, status, error) {
            console.log('error =', error)
        }
    })
}


function SendGet() {

    console.log(document.forms.ShopForm.elements.cps_email.value);
    console.log(document.forms.ShopForm.elements.cps_phone.value);
    console.log(document.forms.ShopForm.elements.orderNumber.value);
    console.log(document.forms.ShopForm.elements.customerNumber.value);

	$.ajax({
		type:'post',//тип запроса: get,post либо head
		url:'processed/',//url адрес файла обработчика
		data:{'cps_email': document.forms.ShopForm.elements.cps_email.value,
              'cps_phone': document.forms.ShopForm.elements.cps_phone.value,
              'orderNumber': document.forms.ShopForm.elements.orderNumber.value,
              'customerNumber': document.forms.ShopForm.elements.customerNumber.value
        },//параметры запроса
		response:'text',//тип возвращаемого ответа text либо xml
		success:function (data) {//возвращаемый результат от сервера
			$.ajax('result',$.ajax('result').innerHTML+'<br />'+data);
		}
	});
}

function SendPost() {
	//отправляю POST запрос и получаю ответ
    var user = detect.parse(navigator.userAgent);
//    var data;
    $.ajax({
       url:'http://freegeoip.net/json/',
       type:'get',
       dataType:'json'
    }).done(function(data) {
       $.ajax({
            type:'post',//тип запроса: get,post либо head
            url:'visitor/',//url адрес файла обработчика
            data:{'browser':user.browser.family,
                  'version': user.browser.version,
                  'os': user.os.name,
                  'device' :user.device.type,
                  'ref' : document.referrer,
                  'addr' : data.ip,
                  'city' : data.city,
                  'region' : data.region_name,
                  'time_zone' : data.time_zone
            },//параметры запроса
            response:'text',//тип возвращаемого ответа text либо xml
            success:function (data) {//возвращаемый результат от сервера

            }
        });
    });


}

