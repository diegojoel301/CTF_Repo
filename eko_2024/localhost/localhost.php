<?php
function curlGetPage($url){
   $ch = curl_init();
   curl_setopt($ch, CURLOPT_URL, $url);
   curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
   curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
   $data = curl_exec($ch);
   return $data;
}
if (isset($_POST['url'])) {
	$url = filter_var($_POST['url'], FILTER_SANITIZE_URL);
    //$url = $_POST['url'];
    //echo $url;
	if (filter_var($url, FILTER_VALIDATE_URL) !== false) {
		$url = urldecode($url);
		if (strstr(strtolower($url), "flag")) {
			die('Unauthorized URL');
		} else {
			echo curlGetPage($url);
		}
	} else {
	    echo("Invalid URL");
	}
}
?>
