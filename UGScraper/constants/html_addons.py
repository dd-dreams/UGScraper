"""
this file has all html tags that is needed to make the outputted html file more prettier
like centering the text and so on

"""

# start of html file
HTML_BASICS_START = """
<!DOCTYPE html>
<html>
    <body>
"""

HTML_BASICS_END = """
    </body>
</html>
"""

CENTER_SMOOTH_TEXT_START = """
    <style>
        html {
            scroll-behavior: smooth;
        }
        div.center {
            text-align: center;
        }   
    </style>
    <div class="center">
"""

CENTER_TEXT_END = "</div>"

AUTO_SCROLL_BUTTON = """
<button onclick="scrollpage()">Autoscroll this GODDAMN PAGE</button>
"""

AUTO_SCROLL_SCRIPT = """
<script>
function scrollpage() {
    var Height=document.documentElement.scrollHeight;
    var i=1;
    function scroll() {
        window.scrollTo(0,i);
        i=i+40;
        if(i>=Height){  return; }
        setTimeout(scroll, 100);
    }scroll();
}
</script>
"""
