<?php
  $format = "%Y'; whoami #";
  $command = "date '+" . $format . "' 2>&1";

  function getTime($command)
  {
    echo $command;
    $time = exec($command);
    $res  = isset($time) ? $time : '?';
    echo " => ".$res;
  }

  getTime($command);
?>

