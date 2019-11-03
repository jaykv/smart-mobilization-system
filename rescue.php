<?php 
require_once 'users/init.php'; 
if (!securePage($_SERVER['PHP_SELF'])){die();}

$db = DB::getInstance();
?>