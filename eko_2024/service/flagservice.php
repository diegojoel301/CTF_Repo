<?php

function getRecords($hostname, $type)
{
	$records = dns_get_record($hostname);
	if ($records !== false) {
		foreach($records as $r) {
			if ($r['type'] == $type) return $r;
		}
	}
	return false;
}

function sendFlag($target, $port) 
{
	$flag = "EKO{SRV_r3c0rd_serving_flags}";
	$fp = fsockopen($target, $port, $errno, $errstr, 30);
        if (!$fp) {
    		echo "$errstr ($errno)";
	} else {
    		fwrite($fp, $flag);
   		fclose($fp);
	}

}

if (isset($_POST['hostname'])) {

	if (filter_var($_POST['hostname'], FILTER_VALIDATE_DOMAIN) !== false) {
		$srv = getRecords($_POST['hostname'], "SRV");
		if ($srv !== false) { 
			sendFlag($srv['target'], $srv['port']);
		} else {
			echo("Service not found");
		}
	} else {
		echo("Invalid hostname");
	}
}
?>