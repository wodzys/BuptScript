 (function() {
    'use strict';
   //return;
    $('table tr').each(function(){
        var lesson = $(this).find("td").eq(1).children('span').text();
            if(lesson == 'Java技术' || lesson == '有效共同技巧（MOOC）'){
                if($(this).children('td').eq(7).children('a').text() != ''){
                    $(this).children('td').eq(7).children('a').trigger('click');

                    console.log(window.frames[0].document.querySelectorAll('input[id=contentParent_dgData_ImageButton1_0]'));
                    setTimeout(function(){
                        $(window.frames[0].document.querySelectorAll('input[id=contentParent_dgData_ImageButton1_0]')).click();
                        $('#contentParent_dgData_ImageButton1_0').click();

                        console.log('chose class now !');
                    }, 2000);
                }
                 else{
                     location.reload();
                 }
            }
        });

   // setTimeout(location.reload(), 10000);

    // Your code here...
})();


function wait_done(){
	if($("iframe[name=selClass]").length > 0){
		window.setTimeout(wait_done,50);
	}else{
		location.reload();
	}
}

function wait_iframe(){
    var ifr = document.getElementsByName('selClass');
    console.log(ifr);
    if(ifr.length == 0)
        window.setTimeout(wait_iframe, 500);
    else{
        var ifrDoc = (ifr[0].contentDocument) ? ifr[0].contentDocument : ifr[0].contentWindow.document;
        if($("iframe[name=selClass]").contents().find('input[id=contentParent_dgData_ImageButton1_0]').length == 0){
			window.setTimeout(wait_iframe,50);
		}else{
			$("iframe[name=selClass]").contents().find('input[id=contentParent_dgData_ImageButton1_0]').trigger('click');
			wait_done();
		}
    }
}


// $("iframe[name=selClass]").contents().find('input[id=contentParent_dgData_ImageButton1_0]').trigger('click');

// $('.Grid_Line>tbody>tr')[1];
$('.Grid_Line>tbody>tr').each(function(){
    var lesson = $(this).find("td").eq(1).text();
    if(lesson.indexOf('认知无线电与认知网络') != -1){
        // console.log('Find course');
        if($(this).children('td').eq(7).children('a').text() != ''){
            $(this).children('td').eq(7).children('a').trigger('click');
            wait_iframe();
        }
        else{
            location.reload();
        }
    }
});

// ClassView('?EID=3YtRb7SM7VqPYigttJ7mfyR1xRcrTkD0QHG373uAzUD384RuRVWaAA==&UID=2019140142','ClassView');
// classFull('?EID=3YtRb7SM7VqPYigttJ7mf8LFLNU3XjQ7LWVnDWdBwP27WrgCpeMKM!UfUAZZFXdic27dA4M!eRU=&UID=2019140142','classFull');


// var EID = '?EID=3YtRb7SM7VqPYigttJ7mf8LFLNU3XjQ7LWVnDWdBwP27WrgCpeMKM!UfUAZZFXdic27dA4M!eRU=&UID=2019140142';
// var dlgid = 'classFull';
// var title = "已选满课程班级";
// var iWidth = 600;
// var iheight = 440;
// var top = '30%';
// var url = "url:/Gstudent/Course/PlanClassSelFull.aspx" + EID;
// $.dialog({
//     top: top,
//     lock: true, content: url, id: dlgid, title: title,
//     min: false, max: true, drag: true, resize: true,
//     width: iWidth, height: iheight,
//     close: function () {
//         clse();
//     }
// });