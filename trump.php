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

.twitter-profile:visited, .twitter-profile:link {
	color: black;
	font-weight: bold;
	text-decoration: none;
	z-index: 10
}

.twitter-profile:hover {
	opacity: 0.5;
}

.username {
	color: gray;
	font-weight: normal;
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
	display: table-cell;
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

</style>
</head>
<body>
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
</body>
</html>