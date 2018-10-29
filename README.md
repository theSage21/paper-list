Paper-List
==========

Maintains a list of papers that I have read. Also notes on those papers.


Tampermonkey
-----------


```javascript
// ==UserScript==
// @name         ArxivLog
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://arxiv.org/*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    function post(url, data, success){
        var data = JSON.stringify(data);
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.withCredentials = true;
        xmlhttp.onreadystatechange = function(){
                    if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
                                    var dat = JSON.parse(xmlhttp.responseText);
                                    success(dat);
                                 }
                 }
        xmlhttp.send(data);
    }
    post('https://paper-list.herokuapp.com/add_paper',
         {'url': document.location.href, 'comment': ''},
         function (d){
            console.log(d);
    });
})();
```
