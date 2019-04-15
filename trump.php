<!DOCTYPE html>
<html>
<head>
<title>AKamienski</title>
<?php include '/var/www/html/start.php'; ?>

<style>
<?php include '/var/www/html/pageStyle.css'; ?>

/* width */
::-webkit-scrollbar {
    width: 2px;
    height: 2px
}

/* Track */
::-webkit-scrollbar-track {
    background: #f1f1f1; 
}

/* Handle */
::-webkit-scrollbar-thumb {
    background: #888; 
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
    background: #555; 
}

a:visited, a:link {
	color: gray;
	text-decoration: none;
}

.twitter-title:visited, .twitter-title:link, .article-title:visited, .article-title:link {
	color: black;
	font-weight: bold;
	text-decoration: none;
}
.twitter-title:hover, .article-title:hover {
	opacity: 1.0;
}


.screen-name, .author, .time {
	color: gray;
	font-weight: normal;
}

.time {
	float: right;
}

.twitter-title:hover > .username, img:hover {
	opacity: 0.5;
}

.article-title:hover > .headline, img:hover {
	opacity: 0.5;
}

#main {
	width: 90%;
	height: 500px
}

img {
	border-radius: 50%;
	object-fit: cover;
	width:60px;
	height:60px;
}

.cell {
	border-bottom-style: solid;
	border-width: 1px;
	border-color: lightgrey;
	
	padding: 10px;
	overflow-x: auto;
}

.cell:hover {
	background-color: ghostwhite;
}

.cell-img, .cell-content{
	display: table-cell;
	vertical-align: top;
	text-align: left;
	width: 10%
}

.cell-content {
	padding-left: 5%;

	width: 100%;
}

.cell-header {
	padding-bottom: 5px;
	width: 100%
}

.feed {
	height: 80%;
	width: 100%;

	overflow-y: auto;
	overflow-x: hidden;
}

#twitter, #cnn {
	padding: 1%;
	height: 100%;
	width: 48%;
	float: left;
}

#cnn {
	float: right;
}

[class~='cell']:last-of-type {
    border-bottom-style: none;
}

.cell-info {
    text-align: right;
    color: grey;
}

#info-panel {
    text-align: center;
    display: none;
    position: fixed;
    margin: 0 auto;
    left: 0;
    right: 0;
    background-color: ghostwhite;
    width: 50%;
    height: 90%;
    z-index: 10;
    overflow-y: auto;
}

#close-button {
    position: absolute;
    top: 1%;
    right: 1%;
    cursor: pointer;
    font-size: 25px;
    float:right;
}

.related-rate {
	float: left;
	opacity: 0.7;
}

.info-button {
	cursor: pointer;
}

#close-button:hover, #related-tweets:hover, #related-articles:hover, .info-button:hover, a:hover {
    opacity: 0.5;
}

#related-tweets, #related-articles {
	cursor: pointer;
}

#panel-header {
    width: 100%;
    height: 7%;
    padding-right: 1%;
    text-align: center;
}

#panel-content, #panel-related, #panel-additional {
    text-align: center;
    width: 95%;
    margin: 0 auto;
    left: 0;
    right: 0;
    border-bottom-style: solid;
    border-color: lightgrey;
    border-width: 2px;
    padding-bottom: 10px;
}

.additional {
	display: none;
}

</style>
</head>
<body>
	<div id='info-panel'>
	    <div id='panel-header'>
	        <h1 class="w3-large">FURTHER INFO</h1>
	        <span id='close-button' onclick='hidediv()'>&#10006;</span>
	    </div> 
	    <div id='panel-content'>
	        
	    </div>
	    <h1 class="w3-large">MORE INFO</h1>
	    <div id='panel-additional'>
	    	
	    </div>

	    <h1 class="w3-large">
	    	RELATED 
	    	<span id='related-tweets' onclick="switch_feed()">TWEETS</span>
	    	<span id='related-articles' onclick="switch_feed()">ARTICLES</span>
	    </h1>
	    <div id='panel-related'>
	    
	    </div>
	</div>

	<div id='dimmer'>
	    <?php include '/var/www/html/header.php'; ?>
		<center>
			<div id="main">
				<h1 class="w3-xlarge">TRUMP FEED</h1>
				<div id='twitter'>
					<h2 class="w3-xlarge">TWEETS</h2>
	                <?php
	                    putenv("PYTHONIOENCODING=utf-8");

	                    $command = escapeshellcmd('/var/www/html/trump_feed_files/twitter_feed.py');

	                    $output = shell_exec($command);
	                    echo $output;
	                ?>
				</div>
				<div id='cnn'>
					<h2 class="w3-xlarge">CNN NEWS</h2>
	                <?php
	                    $command = escapeshellcmd('/var/www/html/trump_feed_files/cnn_feed.py');

	                    $output = shell_exec($command);
	                    echo $output;
	                ?>
				</div>
			</div>
		</center>
	    <?php include '/var/www/html/footer.php'; ?>
	</div>

	<script type="text/javascript">
        // global vars (DOMs)
        var panel = document.getElementById('info-panel');
        var content = document.getElementById('panel-content');
        var related = document.getElementById('panel-related');
        var additional = document.getElementById('panel-additional');
        var twitter = document.getElementById('twitter-feed');
        var cnn = document.getElementById('cnn-feed');
        var dimmer = document.getElementById('dimmer');

        // For panel switching
        var curr_cell = null;
        var feed = null;

        // show the panel div
        function makediv(name, source) {
        	panel.scrollTop = 0;
        	curr_cell = name;

            panel.style.display = 'block';

            dimmer.style.opacity = '0.5';
            dimmer.style.pointerEvents = 'none';
            dimmer.style.overflowY = 'hidden';

            content.innerHTML = document.getElementById(name).outerHTML;
            additional.innerHTML = document.getElementById(name+'-additional').innerHTML;

            if (source == 'twitter') {
            	feed = twitter;
            } else {
            	feed = cnn;
            }

            switch_feed();
        }

        // generate trigrams (3-char strings)
        function trigrams(text) {
            var words = new Set()

            for (var i = 0; i < text.length-2; i++) {
                words.add(text.substring(i, i+3))
            }

            return words
        }

        // build the related section of the panel
        function make_related_to() {
        	var text = document.getElementById(curr_cell+'-text').innerHTML

            var related_list = [];

            var text_trigrams = trigrams(text);

            for (var i = 0; i < feed.childNodes.length; i++) {

                node = feed.childNodes[i];

                if (node.className == 'cell') {
                    
                    node_text = document.getElementById(node.id+'-text').innerHTML;

                    node_trigrams = trigrams(node_text);

                    // Jaccard similarity
                    var similarity = intersect(node_trigrams, text_trigrams)/union(node_trigrams, text_trigrams);

                    if (similarity != 1) {
                    	related_list.push([similarity, node.cloneNode(true)]);
                    }
                }

            }

            // sort by similarity
            related_list.sort(function(a,b){return b[0] - a[0];});

            var cells = [];

            for (var r of related_list.slice(0, 5)) {
            	var sim = r[0];
            	var cell = r[1];

            	var info = cell.querySelector(".cell-info");


            	// related rating formatting
            	if (sim < 0.1) {
            		info.innerHTML = "<span class='related-rate' style='color:red;'>Possibly not related</span>" + info.innerHTML;
            	} else if (sim < 0.15) {
            		info.innerHTML = "<span class='related-rate' style='color:orange;'>Not so related</span>" + info.innerHTML;
            	}  else {
            		info.innerHTML = "<span class='related-rate' style='color:green;'>Possibly Related</span>" + info.innerHTML;
            	}

            	info = document.getElementById(cell.id + '-info');

            	cells.push(cell.outerHTML);
            }

            related.innerHTML = cells
        }

        // helper functions for jaccard similarity
        function union(setA, setB) {
            var u = new Set(setA);
            for (var elem of setB) {
                u.add(elem);
            }

            return u.size;
        }

        function intersect(setA, setB) {
            var i = new Set();
            for (var elem of setB) {
                if (setA.has(elem)) {
                    i.add(elem);
                }
            }

            return i.size;
        }

        // hide panel after close event
        function hidediv() {
            panel.style.display = 'none';
            dimmer.style.opacity = '1.0';
            dimmer.style.pointerEvents = 'auto';
            dimmer.style.overflowY = 'auto';
        }

        // close panel on ESC
        document.addEventListener("keydown", keyPress, false);

        function keyPress (e) {
		    if(e.key === "Escape") {
		        hidediv();
		    }
		}

		// switch related feed from news to tweets and vice-versa
		function switch_feed() {
			var articles = document.getElementById('related-articles');
			var tweets = document.getElementById('related-tweets');

			if(feed === twitter) {

				tweets.style.fontWeight = 'normal';
				tweets.style.color = 'lightgrey';
				
				articles.style.fontWeight = 'bold'
				articles.style.color = 'black';

				feed = cnn;
				make_related_to();
			} else {
				tweets.style.fontWeight = 'bold';
				tweets.style.color = 'black';

				articles.style.fontWeight = 'normal'
				articles.style.color = 'lightgrey';
				feed = twitter;
				make_related_to();
			}
		}

    </script>

</body>
</html>