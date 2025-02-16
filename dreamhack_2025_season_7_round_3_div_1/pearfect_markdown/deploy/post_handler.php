<?php
$uploads_dir = 'uploads/';

if ($_SERVER['REQUEST_METHOD'] === 'GET') {

    $file = $_GET['file'] ?? 'example.md';
    $path = $uploads_dir . $file; 

    include($path);

} else {
    echo "Use GET method!!";
}
?>
