<?php
class TimeModel
{
    public function __construct($format)
    {

        $this->command = "date '+" . $format . "' 2>&1";

    }

    public function getTime()
    {
        echo $this->command;
        $time = exec($this->command);
        $res  = isset($time) ? $time : '?';
        return $res;
    }
}
